-- MySQL dump 10.13  Distrib 5.6.22, for osx10.8 (x86_64)
--
-- Host: localhost    Database: rnaseqdb
-- ------------------------------------------------------
-- Server version	5.6.22

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_0e939a4f` (`group_id`),
  KEY `auth_group_permissions_8373b171` (`permission_id`),
  CONSTRAINT `auth_group_permissi_permission_id_84c5c92e_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_01ab375a_uniq` (`content_type_id`,`codename`),
  KEY `auth_permission_417f1b1c` (`content_type_id`),
  CONSTRAINT `auth_permissi_content_type_id_2f476e4b_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=91 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add permission',2,'add_permission'),(5,'Can change permission',2,'change_permission'),(6,'Can delete permission',2,'delete_permission'),(7,'Can add group',3,'add_group'),(8,'Can change group',3,'change_group'),(9,'Can delete group',3,'delete_group'),(10,'Can add user',4,'add_user'),(11,'Can change user',4,'change_user'),(12,'Can delete user',4,'delete_user'),(13,'Can add content type',5,'add_contenttype'),(14,'Can change content type',5,'change_contenttype'),(15,'Can delete content type',5,'delete_contenttype'),(16,'Can add session',6,'add_session'),(17,'Can change session',6,'change_session'),(18,'Can delete session',6,'delete_session'),(19,'Can add project',7,'add_project'),(20,'Can change project',7,'change_project'),(21,'Can delete project',7,'delete_project'),(22,'Can add file type',8,'add_filetype'),(23,'Can change file type',8,'change_filetype'),(24,'Can delete file type',8,'delete_filetype'),(25,'Can add data file',9,'add_datafile'),(26,'Can change data file',9,'change_datafile'),(27,'Can delete data file',9,'delete_datafile'),(28,'Can add sample detail',10,'add_sampledetail'),(29,'Can change sample detail',10,'change_sampledetail'),(30,'Can delete sample detail',10,'delete_sampledetail'),(31,'Can add job status code',11,'add_jobstatuscode'),(32,'Can change job status code',11,'change_jobstatuscode'),(33,'Can delete job status code',11,'delete_jobstatuscode'),(34,'Can add submitted job type',12,'add_submittedjobtype'),(35,'Can change submitted job type',12,'change_submittedjobtype'),(36,'Can delete submitted job type',12,'delete_submittedjobtype'),(37,'Can add adjust method',13,'add_adjustmethod'),(38,'Can change adjust method',13,'change_adjustmethod'),(39,'Can delete adjust method',13,'delete_adjustmethod'),(40,'Can add normalization method',14,'add_normalizationmethod'),(41,'Can change normalization method',14,'change_normalizationmethod'),(42,'Can delete normalization method',14,'delete_normalizationmethod'),(43,'Can add analysis detail',15,'add_analysisdetail'),(44,'Can change analysis detail',15,'change_analysisdetail'),(45,'Can delete analysis detail',15,'delete_analysisdetail'),(46,'Can add analysis result file',16,'add_analysisresultfile'),(47,'Can change analysis result file',16,'change_analysisresultfile'),(48,'Can delete analysis result file',16,'delete_analysisresultfile'),(49,'Can add analysis plot',17,'add_analysisplot'),(50,'Can change analysis plot',17,'change_analysisplot'),(51,'Can delete analysis plot',17,'delete_analysisplot'),(52,'Can add design factor',18,'add_designfactor'),(53,'Can change design factor',18,'change_designfactor'),(54,'Can delete design factor',18,'delete_designfactor'),(55,'Can add limma contrast',19,'add_limmacontrast'),(56,'Can change limma contrast',19,'change_limmacontrast'),(57,'Can delete limma contrast',19,'delete_limmacontrast'),(58,'Can add submitted job',20,'add_submittedjob'),(59,'Can change submitted job',20,'change_submittedjob'),(60,'Can delete submitted job',20,'delete_submittedjob'),(61,'Can add column type',21,'add_columntype'),(62,'Can change column type',21,'change_columntype'),(63,'Can delete column type',21,'delete_columntype'),(64,'Can add task state',22,'add_taskmeta'),(65,'Can change task state',22,'change_taskmeta'),(66,'Can delete task state',22,'delete_taskmeta'),(67,'Can add saved group result',23,'add_tasksetmeta'),(68,'Can change saved group result',23,'change_tasksetmeta'),(69,'Can delete saved group result',23,'delete_tasksetmeta'),(70,'Can add interval',24,'add_intervalschedule'),(71,'Can change interval',24,'change_intervalschedule'),(72,'Can delete interval',24,'delete_intervalschedule'),(73,'Can add crontab',25,'add_crontabschedule'),(74,'Can change crontab',25,'change_crontabschedule'),(75,'Can delete crontab',25,'delete_crontabschedule'),(76,'Can add periodic tasks',26,'add_periodictasks'),(77,'Can change periodic tasks',26,'change_periodictasks'),(78,'Can delete periodic tasks',26,'delete_periodictasks'),(79,'Can add periodic task',27,'add_periodictask'),(80,'Can change periodic task',27,'change_periodictask'),(81,'Can delete periodic task',27,'delete_periodictask'),(82,'Can add worker',28,'add_workerstate'),(83,'Can change worker',28,'change_workerstate'),(84,'Can delete worker',28,'delete_workerstate'),(85,'Can add task',29,'add_taskstate'),(86,'Can change task',29,'change_taskstate'),(87,'Can delete task',29,'delete_taskstate'),(88,'Can add registration profile',30,'add_registrationprofile'),(89,'Can change registration profile',30,'change_registrationprofile'),(90,'Can delete registration profile',30,'delete_registrationprofile');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$24000$c7oJaHGyFyo7$6EQQLKab5Rk6MXUVIz5bZIn/fo0Ejlq1SNaxceM9wQo=','2016-04-22 23:26:43.350442',1,'a','','','a@a.com',1,1,'2016-04-22 23:24:23.196534'),(2,'pbkdf2_sha256$24000$uqQFLAIRdLX0$PvzLxyzaNEo2xGmop3Wp0I9NfUmjLydAbRQ/N9rVxu8=',NULL,0,'105','','','',0,1,'2016-04-22 23:27:04.513720');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_e8701ad4` (`user_id`),
  KEY `auth_user_groups_0e939a4f` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permissions_e8701ad4` (`user_id`),
  KEY `auth_user_user_permissions_8373b171` (`permission_id`),
  CONSTRAINT `auth_user_user_perm_permission_id_1fbb5f2c_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `celery_taskmeta`
--

DROP TABLE IF EXISTS `celery_taskmeta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `celery_taskmeta` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `task_id` varchar(255) NOT NULL,
  `status` varchar(50) NOT NULL,
  `result` longtext,
  `date_done` datetime(6) NOT NULL,
  `traceback` longtext,
  `hidden` tinyint(1) NOT NULL,
  `meta` longtext,
  PRIMARY KEY (`id`),
  UNIQUE KEY `task_id` (`task_id`),
  KEY `celery_taskmeta_662f707d` (`hidden`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `celery_taskmeta`
--

LOCK TABLES `celery_taskmeta` WRITE;
/*!40000 ALTER TABLE `celery_taskmeta` DISABLE KEYS */;
/*!40000 ALTER TABLE `celery_taskmeta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `celery_tasksetmeta`
--

DROP TABLE IF EXISTS `celery_tasksetmeta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `celery_tasksetmeta` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `taskset_id` varchar(255) NOT NULL,
  `result` longtext NOT NULL,
  `date_done` datetime(6) NOT NULL,
  `hidden` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `taskset_id` (`taskset_id`),
  KEY `celery_tasksetmeta_662f707d` (`hidden`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `celery_tasksetmeta`
--

LOCK TABLES `celery_tasksetmeta` WRITE;
/*!40000 ALTER TABLE `celery_tasksetmeta` DISABLE KEYS */;
/*!40000 ALTER TABLE `celery_tasksetmeta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_417f1b1c` (`content_type_id`),
  KEY `django_admin_log_e8701ad4` (`user_id`),
  CONSTRAINT `django_admin__content_type_id_c4bce8eb_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2016-04-22 23:27:04.590651','2','105',1,'Added.',4,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(25,'djcelery','crontabschedule'),(24,'djcelery','intervalschedule'),(27,'djcelery','periodictask'),(26,'djcelery','periodictasks'),(22,'djcelery','taskmeta'),(23,'djcelery','tasksetmeta'),(29,'djcelery','taskstate'),(28,'djcelery','workerstate'),(30,'registration','registrationprofile'),(13,'rnaseq','adjustmethod'),(15,'rnaseq','analysisdetail'),(17,'rnaseq','analysisplot'),(16,'rnaseq','analysisresultfile'),(21,'rnaseq','columntype'),(9,'rnaseq','datafile'),(18,'rnaseq','designfactor'),(8,'rnaseq','filetype'),(11,'rnaseq','jobstatuscode'),(19,'rnaseq','limmacontrast'),(14,'rnaseq','normalizationmethod'),(7,'rnaseq','project'),(10,'rnaseq','sampledetail'),(20,'rnaseq','submittedjob'),(12,'rnaseq','submittedjobtype'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2016-04-22 23:23:04.697124'),(2,'auth','0001_initial','2016-04-22 23:23:09.228700'),(3,'admin','0001_initial','2016-04-22 23:23:10.209347'),(4,'admin','0002_logentry_remove_auto_add','2016-04-22 23:23:10.606011'),(5,'contenttypes','0002_remove_content_type_name','2016-04-22 23:23:11.085156'),(6,'auth','0002_alter_permission_name_max_length','2016-04-22 23:23:11.295831'),(7,'auth','0003_alter_user_email_max_length','2016-04-22 23:23:11.550574'),(8,'auth','0004_alter_user_username_opts','2016-04-22 23:23:11.561456'),(9,'auth','0005_alter_user_last_login_null','2016-04-22 23:23:11.726544'),(10,'auth','0006_require_contenttypes_0002','2016-04-22 23:23:11.728643'),(11,'auth','0007_alter_validators_add_error_messages','2016-04-22 23:23:11.740657'),(12,'djcelery','0001_initial','2016-04-22 23:23:15.703292'),(13,'registration','0001_initial','2016-04-22 23:23:16.009192'),(14,'rnaseq','0001_initial','2016-04-22 23:23:24.746774'),(15,'sessions','0001_initial','2016-04-22 23:23:25.154234');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_de54fa62` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('6ci0dokj0uw3w6iueoob773ze9zhz5ct','NDFkNjkyMTRjNjQ0ZDY1NWU4MGZlY2RlYzViYWViMzFiMWQ0MTFhMTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJkMmY4YWJmNjNjM2Y1NDMxMzZiMTZiN2Q4NmE2M2E1Nzg2YjFlNDM2In0=','2016-05-06 23:26:43.387496');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `djcelery_crontabschedule`
--

DROP TABLE IF EXISTS `djcelery_crontabschedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `djcelery_crontabschedule` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `minute` varchar(64) NOT NULL,
  `hour` varchar(64) NOT NULL,
  `day_of_week` varchar(64) NOT NULL,
  `day_of_month` varchar(64) NOT NULL,
  `month_of_year` varchar(64) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `djcelery_crontabschedule`
--

LOCK TABLES `djcelery_crontabschedule` WRITE;
/*!40000 ALTER TABLE `djcelery_crontabschedule` DISABLE KEYS */;
/*!40000 ALTER TABLE `djcelery_crontabschedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `djcelery_intervalschedule`
--

DROP TABLE IF EXISTS `djcelery_intervalschedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `djcelery_intervalschedule` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `every` int(11) NOT NULL,
  `period` varchar(24) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `djcelery_intervalschedule`
--

LOCK TABLES `djcelery_intervalschedule` WRITE;
/*!40000 ALTER TABLE `djcelery_intervalschedule` DISABLE KEYS */;
/*!40000 ALTER TABLE `djcelery_intervalschedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `djcelery_periodictask`
--

DROP TABLE IF EXISTS `djcelery_periodictask`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `djcelery_periodictask` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `task` varchar(200) NOT NULL,
  `args` longtext NOT NULL,
  `kwargs` longtext NOT NULL,
  `queue` varchar(200) DEFAULT NULL,
  `exchange` varchar(200) DEFAULT NULL,
  `routing_key` varchar(200) DEFAULT NULL,
  `expires` datetime(6) DEFAULT NULL,
  `enabled` tinyint(1) NOT NULL,
  `last_run_at` datetime(6) DEFAULT NULL,
  `total_run_count` int(10) unsigned NOT NULL,
  `date_changed` datetime(6) NOT NULL,
  `description` longtext NOT NULL,
  `crontab_id` int(11) DEFAULT NULL,
  `interval_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `djcelery_peri_crontab_id_75609bab_fk_djcelery_crontabschedule_id` (`crontab_id`),
  KEY `djcelery_pe_interval_id_b426ab02_fk_djcelery_intervalschedule_id` (`interval_id`),
  CONSTRAINT `djcelery_pe_interval_id_b426ab02_fk_djcelery_intervalschedule_id` FOREIGN KEY (`interval_id`) REFERENCES `djcelery_intervalschedule` (`id`),
  CONSTRAINT `djcelery_peri_crontab_id_75609bab_fk_djcelery_crontabschedule_id` FOREIGN KEY (`crontab_id`) REFERENCES `djcelery_crontabschedule` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `djcelery_periodictask`
--

LOCK TABLES `djcelery_periodictask` WRITE;
/*!40000 ALTER TABLE `djcelery_periodictask` DISABLE KEYS */;
/*!40000 ALTER TABLE `djcelery_periodictask` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `djcelery_periodictasks`
--

DROP TABLE IF EXISTS `djcelery_periodictasks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `djcelery_periodictasks` (
  `ident` smallint(6) NOT NULL,
  `last_update` datetime(6) NOT NULL,
  PRIMARY KEY (`ident`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `djcelery_periodictasks`
--

LOCK TABLES `djcelery_periodictasks` WRITE;
/*!40000 ALTER TABLE `djcelery_periodictasks` DISABLE KEYS */;
/*!40000 ALTER TABLE `djcelery_periodictasks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `djcelery_taskstate`
--

DROP TABLE IF EXISTS `djcelery_taskstate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `djcelery_taskstate` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `state` varchar(64) NOT NULL,
  `task_id` varchar(36) NOT NULL,
  `name` varchar(200) DEFAULT NULL,
  `tstamp` datetime(6) NOT NULL,
  `args` longtext,
  `kwargs` longtext,
  `eta` datetime(6) DEFAULT NULL,
  `expires` datetime(6) DEFAULT NULL,
  `result` longtext,
  `traceback` longtext,
  `runtime` double DEFAULT NULL,
  `retries` int(11) NOT NULL,
  `hidden` tinyint(1) NOT NULL,
  `worker_id` int(11),
  PRIMARY KEY (`id`),
  UNIQUE KEY `task_id` (`task_id`),
  KEY `djcelery_taskstate_9ed39e2e` (`state`),
  KEY `djcelery_taskstate_b068931c` (`name`),
  KEY `djcelery_taskstate_863bb2ee` (`tstamp`),
  KEY `djcelery_taskstate_662f707d` (`hidden`),
  KEY `djcelery_taskstate_ce77e6ef` (`worker_id`),
  CONSTRAINT `djcelery_taskstate_worker_id_f7f57a05_fk_djcelery_workerstate_id` FOREIGN KEY (`worker_id`) REFERENCES `djcelery_workerstate` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `djcelery_taskstate`
--

LOCK TABLES `djcelery_taskstate` WRITE;
/*!40000 ALTER TABLE `djcelery_taskstate` DISABLE KEYS */;
/*!40000 ALTER TABLE `djcelery_taskstate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `djcelery_workerstate`
--

DROP TABLE IF EXISTS `djcelery_workerstate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `djcelery_workerstate` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hostname` varchar(255) NOT NULL,
  `last_heartbeat` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `hostname` (`hostname`),
  KEY `djcelery_workerstate_f129901a` (`last_heartbeat`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `djcelery_workerstate`
--

LOCK TABLES `djcelery_workerstate` WRITE;
/*!40000 ALTER TABLE `djcelery_workerstate` DISABLE KEYS */;
/*!40000 ALTER TABLE `djcelery_workerstate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `registration_registrationprofile`
--

DROP TABLE IF EXISTS `registration_registrationprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `registration_registrationprofile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `activation_key` varchar(40) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `registration_registrationprofil_user_id_5fcbf725_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `registration_registrationprofile`
--

LOCK TABLES `registration_registrationprofile` WRITE;
/*!40000 ALTER TABLE `registration_registrationprofile` DISABLE KEYS */;
/*!40000 ALTER TABLE `registration_registrationprofile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rnaseq_adjustmethod`
--

DROP TABLE IF EXISTS `rnaseq_adjustmethod`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rnaseq_adjustmethod` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) NOT NULL,
  `description` varchar(512) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rnaseq_adjustmethod`
--

LOCK TABLES `rnaseq_adjustmethod` WRITE;
/*!40000 ALTER TABLE `rnaseq_adjustmethod` DISABLE KEYS */;
/*!40000 ALTER TABLE `rnaseq_adjustmethod` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rnaseq_analysisdetail`
--

DROP TABLE IF EXISTS `rnaseq_analysisdetail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rnaseq_analysisdetail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `description` varchar(255) NOT NULL,
  `sample` varchar(255) NOT NULL,
  `block` varchar(255) DEFAULT NULL,
  `logFoldChangeDecideTests` double DEFAULT NULL,
  `pValueCutOffDecideTests` double DEFAULT NULL,
  `dataFile_id` int(11) NOT NULL,
  `normalizationMethod_id` int(11),
  PRIMARY KEY (`id`),
  KEY `rnaseq_analysisdetail_33c46dc4` (`dataFile_id`),
  KEY `rnaseq_analysisdetail_6521e3ec` (`normalizationMethod_id`),
  CONSTRAINT `D8e4bbb3a3541eff1a817d99b4208998` FOREIGN KEY (`normalizationMethod_id`) REFERENCES `rnaseq_normalizationmethod` (`id`),
  CONSTRAINT `rnaseq_analysisdetail_dataFile_id_61b0d34f_fk_rnaseq_datafile_id` FOREIGN KEY (`dataFile_id`) REFERENCES `rnaseq_datafile` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rnaseq_analysisdetail`
--

LOCK TABLES `rnaseq_analysisdetail` WRITE;
/*!40000 ALTER TABLE `rnaseq_analysisdetail` DISABLE KEYS */;
/*!40000 ALTER TABLE `rnaseq_analysisdetail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rnaseq_analysisplot`
--

DROP TABLE IF EXISTS `rnaseq_analysisplot`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rnaseq_analysisplot` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  `plotPath` varchar(255) NOT NULL,
  `plotFileName` varchar(128) NOT NULL,
  `analysisDetail_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `rnaseq_an_analysisDetail_id_6296727f_fk_rnaseq_analysisdetail_id` (`analysisDetail_id`),
  CONSTRAINT `rnaseq_an_analysisDetail_id_6296727f_fk_rnaseq_analysisdetail_id` FOREIGN KEY (`analysisDetail_id`) REFERENCES `rnaseq_analysisdetail` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rnaseq_analysisplot`
--

LOCK TABLES `rnaseq_analysisplot` WRITE;
/*!40000 ALTER TABLE `rnaseq_analysisplot` DISABLE KEYS */;
/*!40000 ALTER TABLE `rnaseq_analysisplot` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rnaseq_analysisresultfile`
--

DROP TABLE IF EXISTS `rnaseq_analysisresultfile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rnaseq_analysisresultfile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  `filePath` varchar(255) NOT NULL,
  `resultFileName` varchar(128) NOT NULL,
  `analysisDetail_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `rnaseq_an_analysisDetail_id_bd8a3846_fk_rnaseq_analysisdetail_id` (`analysisDetail_id`),
  CONSTRAINT `rnaseq_an_analysisDetail_id_bd8a3846_fk_rnaseq_analysisdetail_id` FOREIGN KEY (`analysisDetail_id`) REFERENCES `rnaseq_analysisdetail` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rnaseq_analysisresultfile`
--

LOCK TABLES `rnaseq_analysisresultfile` WRITE;
/*!40000 ALTER TABLE `rnaseq_analysisresultfile` DISABLE KEYS */;
/*!40000 ALTER TABLE `rnaseq_analysisresultfile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rnaseq_columntype`
--

DROP TABLE IF EXISTS `rnaseq_columntype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rnaseq_columntype` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) NOT NULL,
  `description` varchar(512) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rnaseq_columntype`
--

LOCK TABLES `rnaseq_columntype` WRITE;
/*!40000 ALTER TABLE `rnaseq_columntype` DISABLE KEYS */;
INSERT INTO `rnaseq_columntype` VALUES (1,'factor','factor'),(2,'block','block'),(3,'sample','sample');
/*!40000 ALTER TABLE `rnaseq_columntype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rnaseq_datafile`
--

DROP TABLE IF EXISTS `rnaseq_datafile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rnaseq_datafile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) NOT NULL,
  `description` varchar(512) NOT NULL,
  `uploadedDate` datetime(6) DEFAULT NULL,
  `filePath` varchar(512) NOT NULL,
  `fileType_id` int(11),
  `project_id` int(11) NOT NULL,
  `uploadedBy_id` int(11),
  PRIMARY KEY (`id`),
  KEY `rnaseq_datafile_f379dfbc` (`fileType_id`),
  KEY `rnaseq_datafile_b098ad43` (`project_id`),
  KEY `rnaseq_datafile_a2e019e7` (`uploadedBy_id`),
  CONSTRAINT `rnaseq_datafile_fileType_id_0b28e69d_fk_rnaseq_filetype_id` FOREIGN KEY (`fileType_id`) REFERENCES `rnaseq_filetype` (`id`),
  CONSTRAINT `rnaseq_datafile_project_id_e00eba7b_fk_rnaseq_project_id` FOREIGN KEY (`project_id`) REFERENCES `rnaseq_project` (`id`),
  CONSTRAINT `rnaseq_datafile_uploadedBy_id_be3b6a43_fk_auth_user_id` FOREIGN KEY (`uploadedBy_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rnaseq_datafile`
--

LOCK TABLES `rnaseq_datafile` WRITE;
/*!40000 ALTER TABLE `rnaseq_datafile` DISABLE KEYS */;
/*!40000 ALTER TABLE `rnaseq_datafile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rnaseq_designfactor`
--

DROP TABLE IF EXISTS `rnaseq_designfactor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rnaseq_designfactor` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  `description` varchar(255) NOT NULL,
  `analysisDetail_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `rnaseq_de_analysisDetail_id_dad34dcc_fk_rnaseq_analysisdetail_id` (`analysisDetail_id`),
  CONSTRAINT `rnaseq_de_analysisDetail_id_dad34dcc_fk_rnaseq_analysisdetail_id` FOREIGN KEY (`analysisDetail_id`) REFERENCES `rnaseq_analysisdetail` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rnaseq_designfactor`
--

LOCK TABLES `rnaseq_designfactor` WRITE;
/*!40000 ALTER TABLE `rnaseq_designfactor` DISABLE KEYS */;
/*!40000 ALTER TABLE `rnaseq_designfactor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rnaseq_filetype`
--

DROP TABLE IF EXISTS `rnaseq_filetype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rnaseq_filetype` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) NOT NULL,
  `description` varchar(512) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rnaseq_filetype`
--

LOCK TABLES `rnaseq_filetype` WRITE;
/*!40000 ALTER TABLE `rnaseq_filetype` DISABLE KEYS */;
INSERT INTO `rnaseq_filetype` VALUES (1,'contrastMatrix','ContrastMatrix'),(2,'qcZipFile','Zip of QC files'),(3,'phenotypeFile','Phenotype File');
/*!40000 ALTER TABLE `rnaseq_filetype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rnaseq_jobstatuscode`
--

DROP TABLE IF EXISTS `rnaseq_jobstatuscode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rnaseq_jobstatuscode` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(10) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rnaseq_jobstatuscode`
--

LOCK TABLES `rnaseq_jobstatuscode` WRITE;
/*!40000 ALTER TABLE `rnaseq_jobstatuscode` DISABLE KEYS */;
INSERT INTO `rnaseq_jobstatuscode` VALUES (1,'QUEUE','In Queue'),(2,'START','Started'),(3,'END','Ended'),(4,'TERM','Terminated');
/*!40000 ALTER TABLE `rnaseq_jobstatuscode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rnaseq_limmacontrast`
--

DROP TABLE IF EXISTS `rnaseq_limmacontrast`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rnaseq_limmacontrast` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  `description` varchar(255) NOT NULL,
  `analysisDetail_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `rnaseq_li_analysisDetail_id_ff39cac4_fk_rnaseq_analysisdetail_id` (`analysisDetail_id`),
  CONSTRAINT `rnaseq_li_analysisDetail_id_ff39cac4_fk_rnaseq_analysisdetail_id` FOREIGN KEY (`analysisDetail_id`) REFERENCES `rnaseq_analysisdetail` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rnaseq_limmacontrast`
--

LOCK TABLES `rnaseq_limmacontrast` WRITE;
/*!40000 ALTER TABLE `rnaseq_limmacontrast` DISABLE KEYS */;
/*!40000 ALTER TABLE `rnaseq_limmacontrast` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rnaseq_normalizationmethod`
--

DROP TABLE IF EXISTS `rnaseq_normalizationmethod`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rnaseq_normalizationmethod` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(10) NOT NULL,
  `description` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rnaseq_normalizationmethod`
--

LOCK TABLES `rnaseq_normalizationmethod` WRITE;
/*!40000 ALTER TABLE `rnaseq_normalizationmethod` DISABLE KEYS */;
/*!40000 ALTER TABLE `rnaseq_normalizationmethod` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rnaseq_project`
--

DROP TABLE IF EXISTS `rnaseq_project`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rnaseq_project` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) NOT NULL,
  `startDate` datetime(6) DEFAULT NULL,
  `endDate` datetime(6) DEFAULT NULL,
  `autoLoaded` tinyint(1) DEFAULT NULL,
  `autoLoadedFromPath` varchar(512) DEFAULT NULL,
  `autoLoadedDate` datetime(6) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `rnaseq_project_user_id_fd911c54_fk_auth_user_id` (`user_id`),
  CONSTRAINT `rnaseq_project_user_id_fd911c54_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rnaseq_project`
--

LOCK TABLES `rnaseq_project` WRITE;
/*!40000 ALTER TABLE `rnaseq_project` DISABLE KEYS */;
/*!40000 ALTER TABLE `rnaseq_project` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rnaseq_sampledetail`
--

DROP TABLE IF EXISTS `rnaseq_sampledetail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rnaseq_sampledetail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sampleName` varchar(512) NOT NULL,
  `numberOfInputReads` int(11) NOT NULL,
  `pctUniquelyMappedReads` double NOT NULL,
  `pctMappedMultipleLoci` double NOT NULL,
  `pctUnMappedTooManyLoci` double NOT NULL,
  `pctUnMappedTooManyMismatches` double NOT NULL,
  `pctUnMappedTooShort` double NOT NULL,
  `pctUnMappedOther` double NOT NULL,
  `qcQualiMapHTMLPath` varchar(512) NOT NULL,
  `fastQcHTMLPath` varchar(512) NOT NULL,
  `totalAlignments` int(11) NOT NULL,
  `dataFile_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `rnaseq_sampledetail_dataFile_id_c70eab8c_fk_rnaseq_datafile_id` (`dataFile_id`),
  CONSTRAINT `rnaseq_sampledetail_dataFile_id_c70eab8c_fk_rnaseq_datafile_id` FOREIGN KEY (`dataFile_id`) REFERENCES `rnaseq_datafile` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rnaseq_sampledetail`
--

LOCK TABLES `rnaseq_sampledetail` WRITE;
/*!40000 ALTER TABLE `rnaseq_sampledetail` DISABLE KEYS */;
/*!40000 ALTER TABLE `rnaseq_sampledetail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rnaseq_submittedjob`
--

DROP TABLE IF EXISTS `rnaseq_submittedjob`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rnaseq_submittedjob` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(512) NOT NULL,
  `description` varchar(512) DEFAULT NULL,
  `submittedOn` datetime(6) DEFAULT NULL,
  `downloadDataFileLink` varchar(512) DEFAULT NULL,
  `completedTime` datetime(6) DEFAULT NULL,
  `analysisDetail_id` int(11) DEFAULT NULL,
  `jobStatusCode_id` int(11) NOT NULL,
  `submittedBy_id` int(11) NOT NULL,
  `submittedJobType_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `rnaseq_su_analysisDetail_id_acd37597_fk_rnaseq_analysisdetail_id` (`analysisDetail_id`),
  KEY `rnaseq_subm_jobStatusCode_id_5daf70f5_fk_rnaseq_jobstatuscode_id` (`jobStatusCode_id`),
  KEY `rnaseq_submittedjob_submittedBy_id_a5102f82_fk_auth_user_id` (`submittedBy_id`),
  KEY `rnaseq_submittedjob_f6014265` (`submittedJobType_id`),
  CONSTRAINT `rnase_submittedJobType_id_67dd8cde_fk_rnaseq_submittedjobtype_id` FOREIGN KEY (`submittedJobType_id`) REFERENCES `rnaseq_submittedjobtype` (`id`),
  CONSTRAINT `rnaseq_su_analysisDetail_id_acd37597_fk_rnaseq_analysisdetail_id` FOREIGN KEY (`analysisDetail_id`) REFERENCES `rnaseq_analysisdetail` (`id`),
  CONSTRAINT `rnaseq_subm_jobStatusCode_id_5daf70f5_fk_rnaseq_jobstatuscode_id` FOREIGN KEY (`jobStatusCode_id`) REFERENCES `rnaseq_jobstatuscode` (`id`),
  CONSTRAINT `rnaseq_submittedjob_submittedBy_id_a5102f82_fk_auth_user_id` FOREIGN KEY (`submittedBy_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rnaseq_submittedjob`
--

LOCK TABLES `rnaseq_submittedjob` WRITE;
/*!40000 ALTER TABLE `rnaseq_submittedjob` DISABLE KEYS */;
/*!40000 ALTER TABLE `rnaseq_submittedjob` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rnaseq_submittedjobtype`
--

DROP TABLE IF EXISTS `rnaseq_submittedjobtype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rnaseq_submittedjobtype` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(10) NOT NULL,
  `description` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rnaseq_submittedjobtype`
--

LOCK TABLES `rnaseq_submittedjobtype` WRITE;
/*!40000 ALTER TABLE `rnaseq_submittedjobtype` DISABLE KEYS */;
INSERT INTO `rnaseq_submittedjobtype` VALUES (1,'Download','Create download Zip File'),(2,'Upload','Upload files'),(3,'Analysis','Analysis of data using Limma');
/*!40000 ALTER TABLE `rnaseq_submittedjobtype` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-04-22 19:27:25
