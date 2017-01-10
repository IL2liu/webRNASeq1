import shutil, os, sys, traceback
outPath = "/Users/mitras/projects/data/Project_8"
inPath  = "/Users/mitras/projects/outdata/final"

try:

    for src_dir, dirs, files in os.walk(inPath):
    
        print " src_dir = " + str(src_dir)
        print " dirs = " + str(dirs)
        print " files = " + str(files)

        for file_ in files:
            src_file = os.path.join(inPath, file_)
            dst_file = os.path.join(outPath, file_)
            shutil.copy(src_file, dst_file)

        for dir_ in dirs:
            src_ = os.path.join(src_dir, dir_)
            dst_ = os.path.join(outPath, dir_)
   
            #dst_dir = os.path.join(outPath, dir_)
            shutil.copytree(src_, dst_)

        break
    
    shutil.rmtree(inPath)

except:

    traceback.print_exc(file=sys.stdout)    

    #dst_dir = src_dir.replace(root_src_dir, root_target_dir)
    #if not os.path.exists(dst_dir):
        #os.mkdir(dst_dir)
    #for file_ in files:
        #src_file = os.path.join(src_dir, file_)
        #dst_file = os.path.join(dst_dir, file_)
        #if os.path.exists(dst_file):
            #os.remove(dst_file)
        #if operation is 'copy':
            #shutil.copy(src_file, dst_dir)
        #elif operation is 'move':
            #shutil.move(src_file, dst_dir)