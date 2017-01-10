import json
from functools import reduce

from django.shortcuts import render

from pandas import DataFrame

from seaborn import color_palette, diverging_palette

from bokeh.embed import components
from bokeh.plotting import figure, ColumnDataSource
from bokeh.models import HoverTool, Circle, Panel, Tabs

from reporting.forms import UploadFileForm
from reporting.report import get_user_variants
from reporting.report import roc_curve_data, filter_variants, get_db_data

_SCORE_NAMES = (
    'CADD_raw_rankscore',
    'SIFT_converted_rankscore',
    'Polyphen2_HDIV_rankscore',
)

# Plot values
_WIDTH = 1000  # pixels
_HEIGHT = 700  # pixels
_PLOT_TOOLS = 'pan,box_zoom,resize,wheel_zoom,save,reset'


def report(request):
    '''Generates the report view.'''
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        template_data = {'form': form}

        if form.is_valid():
            in_file = request.FILES['file']

            variants = get_user_variants(in_file.get_records())
            variants = filter_variants(get_db_data(variants), _SCORE_NAMES)

            # === Data for user download

            template_data['json_recs'] = _get_json_recs(variants, _SCORE_NAMES)

            # === Box Plot

            boxplot_data = _boxplot_data(variants, _SCORE_NAMES)
            boxplot_script, boxplot_div = _boxplot(boxplot_data)

            template_data['boxplot_div'] = boxplot_div
            template_data['boxplot_script'] = boxplot_script

            # === Heatmap Plot

            heatmap_data = _heatmap_data(variants, _SCORE_NAMES)
            heat_script, heat_div = _heatmap_plot(heatmap_data)

            template_data['heatmap_div'] = heat_div
            template_data['heatmap_script'] = heat_script

            # === ROC Curve

            data = roc_curve_data(variants, _SCORE_NAMES)
            roc_script, roc_div = _roc_plot(data)

            template_data['roc_curve_div'] = roc_div
            template_data['roc_curve_script'] = roc_script
    else:
        form = UploadFileForm()
        template_data = {'form': form}

    return render(request, 'report.html', template_data)


def _expand_var_records(variant, score_names):
    '''Extracts a list of dicts, with each element of the list representing a
    different score name.'''
    recs = []

    for name in score_names:
        recs.append({
            'genome': variant.get_genome(),
            'chromosome': variant.get_chromosome(),
            'position': variant.get_position(),
            'reference': variant.get_reference(),
            'alternative': variant.get_alternative(),
            'score_name': name,
            'score_value': variant.get_data_val(name),
        })

    return recs


def _get_json_recs(variants, score_names):
    '''Returns a list of dicts, with each dict containing data extracted from
    variants.'''
    return json.dumps(reduce(
        lambda x, y: x + y,
        [_expand_var_records(v, score_names) for v in variants],
        [],
    ))


def _heatmap_plot(data):
    '''Returns a (JS script, div) tuple for plot generation, both in UTF-8.'''
    colors = diverging_palette(220, 20, n=10).as_hex()
    data['color'] = [colors[min(int(x * 10), 9)] for x in data['value']]

    source = ColumnDataSource(data=data)

    heatmap = figure(
        title='Heatmap',
        y_range=list(set(data['score'])),
        plot_width=_WIDTH,
        plot_height=_HEIGHT,
        tools=_PLOT_TOOLS,
    )

    rect = heatmap.rect(
        x='x',
        y='score',
        width=1,
        height=1,
        source=source,
        color='color',
        line_color=None,
    )

    hover = HoverTool(
        renderers=[rect],
        tooltips=[('algorithm', '@score'), ('score', '@value')],
    )

    heatmap.add_tools(hover)

    heatmap.grid.grid_line_color = None
    heatmap.axis.axis_line_color = None
    heatmap.axis.major_tick_line_color = None
    heatmap.axis.major_label_text_font_size = '10pt'
    heatmap.axis.major_label_standoff = 1
    heatmap.xaxis.visible = None

    return components(heatmap)


def _heatmap_data(variants, score_names):
    '''Creates the data structure for the heatmap plot.

    Args:
        variants : A list of Variants.
        score_names : The names of the fields to include on the heatmap. The
                      values for this data must convertable to float.

    Returns a dict with the following key : value pairs:
        - score : List of string indicating score name.
        - value : List of float values of the score.
        - x : List of indices that indicate ordering along the x-axis.
    '''
    variants = list(
        filter(lambda v: v.get_effect_est().get_effect() is not None, variants)
    )

    data = {name: [float(v.get_data_val(name)) for v in variants]
            for name in score_names}

    effects = [v.get_effect_est().get_effect() for v in variants]
    indxs = sorted(range(len(effects)), key=lambda k: effects[k])

    for name in score_names:  # Sort data columns by effect
        data[name] = [data[name][x] for x in indxs]

    data_flattened = {'score': [], 'value': [], 'x': []}

    for name in score_names:
        val_len = len(data[name])
        data_flattened['score'] += [name] * val_len
        data_flattened['value'] += data[name]
        data_flattened['x'] += [str(x) for x in range(val_len)]

    return data_flattened


def _boxplot_data(variants, score_names):
    '''Creates the data structure for the box plot.

    Args:
        variants : A list of Variants.
        score_names : The names of the fields to include on the heatmap. The
                      values for this data must convertable to float.

    Returns a dict of dicts with the following key : value pairs:
        - score name : A dict with the following key : value pairs:
            - effect : A list of effects corresponding to the list of values.
            - value : A list of score values corresponding to the list of
                      effects.
    '''
    data = {name: {'effect': [], 'value': []} for name in score_names}

    for name in score_names:
        vals = [float(v.get_data_val(name)) for v in variants]
        effects = [v.get_effect_est().get_metadata() for v in variants]
        data[name]['effect'] += effects
        data[name]['value'] += vals

    return data


def _boxplot(data):
    '''Returns a (JS script, div) tuple for plot generation, both in UTF-8.'''
    tabs = []

    for k in data:
        df = DataFrame(data[k])

        groups = df.groupby('effect', sort=True)
        categories = [x[0] for x in list(groups)]

        hex_cols = color_palette(n_colors=len(categories)+1).as_hex()

        boxplot_cols = hex_cols[:-1]
        point_col = hex_cols[-1]

        q1 = groups.quantile(q=0.25)
        q2 = groups.quantile(q=0.5)
        q3 = groups.quantile(q=0.75)
        qmin = groups.quantile(q=0.00)
        qmax = groups.quantile(q=1.00)

        iqr = q3 - q1
        upper = q3 + 1.5*iqr
        lower = q1 - 1.5*iqr

        upper.value = [
            min([x, y]) for (x, y) in zip(list(qmax.iloc[:, 0]), upper.value)
        ]

        lower.value = [
            max([x, y]) for (x, y) in zip(list(qmin.iloc[:, 0]), lower.value)
        ]

        boxplot = figure(
            x_range=categories,
            title=k,
            tools=_PLOT_TOOLS,
            width=_WIDTH,
            height=_HEIGHT,
        )

        # Stems
        boxplot.segment(
            categories,
            upper.value,
            categories,
            q3.value,
            line_width=2,
            line_color='black'
        )

        boxplot.segment(
            categories,
            lower.value,
            categories,
            q1.value,
            line_width=2,
            line_color='black'
        )

        width = _WIDTH // len(categories) // 3

        # Boxes
        boxplot.rect(
            x=categories,
            y=(q3.value+q2.value)/2,
            width=width,
            height=q3.value-q2.value,
            fill_color=hex_cols[:-1],
            line_width=1,
            line_color='black',
            width_units='screen',
        )

        boxplot.rect(
            x=categories,
            y=(q2.value+q1.value)/2,
            width=width,
            height=q2.value-q1.value,
            fill_color=boxplot_cols,
            line_width=1,
            line_color='black',
            width_units='screen',
        )

        # Whiskers (almost-0 height rects; simpler than segments)
        whisker_height = 1
        whisker_width = width//2

        boxplot.rect(
            x=categories,
            y=lower.value,
            width=whisker_width,
            height=whisker_height,
            line_color='black',
            width_units='screen',
            height_units='screen',
        )

        boxplot.rect(
            x=categories,
            y=upper.value,
            width=whisker_width,
            height=whisker_height,
            line_color='black',
            width_units='screen',
            height_units='screen',
        )

        # Data points
        boxplot.add_glyph(
            ColumnDataSource(data[k]),
            Circle(
                x='effect',
                y='value',
                fill_color=point_col,
                fill_alpha=0.3,
                line_alpha=0.3,
                size=8,
            )
        )

        boxplot.xgrid.grid_line_color = None
        boxplot.ygrid.grid_line_color = None
        boxplot.xaxis.major_label_text_font_size = '12pt'

        tabs.append(Panel(child=boxplot, title=k))

    return components(Tabs(tabs=tabs))


def _roc_plot(data):
    '''Returns a (JS script, div) tuple for plot generation, both in UTF-8.'''
    roc_curve = figure(
        plot_width=_WIDTH,
        plot_height=_HEIGHT,
        x_axis_label='1 - Specificity',
        y_axis_label='Sensitivity',
        tools=_PLOT_TOOLS,
    )

    hex_cols = color_palette(n_colors=len(data)).as_hex()

    circ_glyphs = []
    leg_txt = '{algo} (AUC: {auc:4.2f}, 95% CI ({lower:4.2f}, {upper:4.2f}))'

    for col, line in zip(hex_cols, data):
        fpr_tpr = line['coords']
        fpr, tpr = zip(*fpr_tpr)

        thres = line['thresholds']

        col_src = ColumnDataSource({
            'fpr': fpr,
            'tpr': tpr,
            'thres': thres,
            'specificity': [1-x for x in fpr]
        })

        lower, auc, upper = line['auc']

        legend = leg_txt.format(
            algo=line['algorithm'],
            auc=auc,
            lower=lower,
            upper=upper,
        )

        roc_curve.line(
            x='fpr',
            y='tpr',
            source=col_src,
            color=col,
            legend=legend,
            line_width=1.5,
        )

        circ_glyphs.append(roc_curve.circle(
            x='fpr',
            y='tpr',
            source=col_src,
            color=col,
            size=6,
            alpha=0.5,
        ))

    # Hover tool display

    tooltips = [
        ('Threshold', '@thres'),
        ('(Specificity, Sensitivity)', '(@specificity, @tpr)'),
    ]

    roc_curve.add_tools(HoverTool(
        tooltips=tooltips,
        renderers=circ_glyphs,
        mode='mouse',
    ))

    # The y = x reference line

    x = [0.03, 0.97]
    roc_curve.line(x, x, color='grey', line_width=0.75, line_dash=[4, 4])

    # High sens/spec region lines

    x, y = [0.225, 0.225], [0, 1]
    roc_curve.line(x, y, color='grey', line_width=0.75, line_dash=[2, 2])

    x, y = [0, 1], [0.775, 0.775]
    roc_curve.line(x, y, color='grey', line_width=0.75, line_dash=[2, 2])

    # Plot annotation

    roc_curve.title = 'ROC Curve'
    roc_curve.grid.grid_line_color = None
    roc_curve.legend.orientation = 'bottom_right'

    return components(roc_curve)
