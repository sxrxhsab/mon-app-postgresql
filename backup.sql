-- MySQL dump 10.13  Distrib 8.0.40, for Linux (x86_64)
--
-- Host: sabeur.mysql.pythonanywhere-services.com    Database: sabeur$default
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Administrateur`
--

DROP TABLE IF EXISTS `Administrateur`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Administrateur` (
  `id_admin` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(100) NOT NULL,
  `prenom` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `mot_de_passe` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id_admin`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Administrateur`
--

LOCK TABLES `Administrateur` WRITE;
/*!40000 ALTER TABLE `Administrateur` DISABLE KEYS */;
INSERT INTO `Administrateur` VALUES (1,'bouhamadouche','safia',NULL,NULL);
/*!40000 ALTER TABLE `Administrateur` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ChefDepartement`
--

DROP TABLE IF EXISTS `ChefDepartement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ChefDepartement` (
  `id_chef` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(100) NOT NULL,
  `prenom` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `id_departement` int DEFAULT NULL,
  `mot_de_passe` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id_chef`),
  KEY `id_departement` (`id_departement`),
  CONSTRAINT `ChefDepartement_ibfk_1` FOREIGN KEY (`id_departement`) REFERENCES `Departement` (`id_departement`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ChefDepartement`
--

LOCK TABLES `ChefDepartement` WRITE;
/*!40000 ALTER TABLE `ChefDepartement` DISABLE KEYS */;
/*!40000 ALTER TABLE `ChefDepartement` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Departement`
--

DROP TABLE IF EXISTS `Departement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Departement` (
  `id_departement` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(100) NOT NULL,
  `responsable` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `telephone` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id_departement`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Departement`
--

LOCK TABLES `Departement` WRITE;
/*!40000 ALTER TABLE `Departement` DISABLE KEYS */;
INSERT INTO `Departement` VALUES (1,'Informatique','Prof. Belkacmi',NULL,NULL),(2,'Mathématiques','Prof. Djedai',NULL,NULL),(3,'Physique','Prof. Smith',NULL,NULL),(4,'Chimie','Prof. Johnson',NULL,NULL),(5,'Biologie','Prof. Wilson',NULL,NULL);
/*!40000 ALTER TABLE `Departement` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Doyen`
--

DROP TABLE IF EXISTS `Doyen`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Doyen` (
  `id_doyen` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(100) NOT NULL,
  `prenom` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `mot_de_passe` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id_doyen`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Doyen`
--

LOCK TABLES `Doyen` WRITE;
/*!40000 ALTER TABLE `Doyen` DISABLE KEYS */;
/*!40000 ALTER TABLE `Doyen` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Etudiant`
--

DROP TABLE IF EXISTS `Etudiant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Etudiant` (
  `id_etudiant` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(100) NOT NULL,
  `prenom` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `id_formation` int DEFAULT NULL,
  `annee` int DEFAULT NULL,
  PRIMARY KEY (`id_etudiant`),
  KEY `id_formation` (`id_formation`),
  CONSTRAINT `Etudiant_ibfk_1` FOREIGN KEY (`id_formation`) REFERENCES `Formation` (`id_formation`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Etudiant`
--

LOCK TABLES `Etudiant` WRITE;
/*!40000 ALTER TABLE `Etudiant` DISABLE KEYS */;
/*!40000 ALTER TABLE `Etudiant` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Examen`
--

DROP TABLE IF EXISTS `Examen`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Examen` (
  `id_examen` int NOT NULL AUTO_INCREMENT,
  `id_module` int DEFAULT NULL,
  `date_exam` date NOT NULL,
  `duree` varchar(20) DEFAULT NULL,
  `id_salle` int DEFAULT NULL,
  `id_prof` int DEFAULT NULL,
  `nb_etudiants` int DEFAULT NULL,
  PRIMARY KEY (`id_examen`),
  KEY `id_module` (`id_module`),
  KEY `id_salle` (`id_salle`),
  KEY `id_prof` (`id_prof`),
  CONSTRAINT `Examen_ibfk_1` FOREIGN KEY (`id_module`) REFERENCES `Module` (`id_module`),
  CONSTRAINT `Examen_ibfk_2` FOREIGN KEY (`id_salle`) REFERENCES `Salle` (`id_salle`),
  CONSTRAINT `Examen_ibfk_3` FOREIGN KEY (`id_prof`) REFERENCES `Professeur` (`id_prof`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Examen`
--

LOCK TABLES `Examen` WRITE;
/*!40000 ALTER TABLE `Examen` DISABLE KEYS */;
INSERT INTO `Examen` VALUES (1,1,'2025-01-20','2h',1,1,120),(2,2,'2025-01-22','3h',2,1,45),(3,3,'2025-01-25','2h',3,2,38),(4,4,'2025-01-28','2h',4,3,52),(5,5,'2025-01-30','3h',5,3,48);
/*!40000 ALTER TABLE `Examen` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Formation`
--

DROP TABLE IF EXISTS `Formation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Formation` (
  `id_formation` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(100) NOT NULL,
  `id_departement` int DEFAULT NULL,
  `niveau` varchar(50) DEFAULT NULL,
  `duree` int DEFAULT NULL,
  PRIMARY KEY (`id_formation`),
  KEY `id_departement` (`id_departement`),
  CONSTRAINT `Formation_ibfk_1` FOREIGN KEY (`id_departement`) REFERENCES `Departement` (`id_departement`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Formation`
--

LOCK TABLES `Formation` WRITE;
/*!40000 ALTER TABLE `Formation` DISABLE KEYS */;
INSERT INTO `Formation` VALUES (1,'Licence Informatique',1,'Licence',NULL),(2,'Master Informatique',1,'Master',NULL),(3,'Licence Mathématiques',2,'Licence',NULL),(4,'Master Mathématiques',2,'Master',NULL),(5,'Licence Physique',3,'Licence',NULL);
/*!40000 ALTER TABLE `Formation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Module`
--

DROP TABLE IF EXISTS `Module`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Module` (
  `id_module` int NOT NULL AUTO_INCREMENT,
  `nom_module` varchar(200) NOT NULL,
  `code_module` varchar(20) DEFAULT NULL,
  `id_formation` int DEFAULT NULL,
  `coefficient` float DEFAULT NULL,
  `credit` int DEFAULT NULL,
  PRIMARY KEY (`id_module`),
  KEY `id_formation` (`id_formation`),
  CONSTRAINT `Module_ibfk_1` FOREIGN KEY (`id_formation`) REFERENCES `Formation` (`id_formation`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Module`
--

LOCK TABLES `Module` WRITE;
/*!40000 ALTER TABLE `Module` DISABLE KEYS */;
INSERT INTO `Module` VALUES (1,'Algorithmique Avancée','INF301',1,3,NULL),(2,'Base de Données','INF302',1,3,NULL),(3,'Réseaux Informatiques','INF303',1,2,NULL),(4,'Algèbre Linéaire','MAT201',3,3,NULL),(5,'Analyse Mathématique','MAT202',3,3,NULL),(6,'Mécanique Quantique','PHY101',5,4,NULL);
/*!40000 ALTER TABLE `Module` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Professeur`
--

DROP TABLE IF EXISTS `Professeur`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Professeur` (
  `id_prof` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(100) NOT NULL,
  `prenom` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `telephone` varchar(20) DEFAULT NULL,
  `specialite` varchar(200) DEFAULT NULL,
  `id_departement` int DEFAULT NULL,
  PRIMARY KEY (`id_prof`),
  KEY `id_departement` (`id_departement`),
  CONSTRAINT `Professeur_ibfk_1` FOREIGN KEY (`id_departement`) REFERENCES `Departement` (`id_departement`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Professeur`
--

LOCK TABLES `Professeur` WRITE;
/*!40000 ALTER TABLE `Professeur` DISABLE KEYS */;
INSERT INTO `Professeur` VALUES (1,'Belkacmi','Ahmed',NULL,NULL,'Informatique',1),(2,'Amir','Samir',NULL,NULL,'Réseaux',1),(3,'Djedai','Karim',NULL,NULL,'Mathématiques',2),(4,'Smith','John',NULL,NULL,'Physique',3),(5,'Johnson','Emily',NULL,NULL,'Chimie',4);
/*!40000 ALTER TABLE `Professeur` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Salle`
--

DROP TABLE IF EXISTS `Salle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Salle` (
  `id_salle` int NOT NULL AUTO_INCREMENT,
  `nom_salle` varchar(50) NOT NULL,
  `type` varchar(50) DEFAULT NULL,
  `capacite` int DEFAULT NULL,
  `equipements` text,
  PRIMARY KEY (`id_salle`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Salle`
--

LOCK TABLES `Salle` WRITE;
/*!40000 ALTER TABLE `Salle` DISABLE KEYS */;
INSERT INTO `Salle` VALUES (1,'A201','Amphi',150,NULL),(2,'B105','Salle',50,NULL),(3,'C304','Salle',40,NULL),(4,'D102','Laboratoire',30,NULL),(5,'E205','Salle',60,NULL);
/*!40000 ALTER TABLE `Salle` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `administrateur`
--

DROP TABLE IF EXISTS `administrateur`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `administrateur` (
  `id_admin` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(50) DEFAULT NULL,
  `prenom` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_admin`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `administrateur`
--

LOCK TABLES `administrateur` WRITE;
/*!40000 ALTER TABLE `administrateur` DISABLE KEYS */;
INSERT INTO `administrateur` VALUES (1,'bouhamadouche','safia'),(2,'gaceb','djamel');
/*!40000 ALTER TABLE `administrateur` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `chef_departement`
--

DROP TABLE IF EXISTS `chef_departement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `chef_departement` (
  `id_chef` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(50) DEFAULT NULL,
  `prenom` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_chef`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chef_departement`
--

LOCK TABLES `chef_departement` WRITE;
/*!40000 ALTER TABLE `chef_departement` DISABLE KEYS */;
INSERT INTO `chef_departement` VALUES (1,'zaid',''),(2,'mssbah','');
/*!40000 ALTER TABLE `chef_departement` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `doyen`
--

DROP TABLE IF EXISTS `doyen`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `doyen` (
  `id_doyen` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(50) DEFAULT NULL,
  `prenom` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_doyen`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `doyen`
--

LOCK TABLES `doyen` WRITE;
/*!40000 ALTER TABLE `doyen` DISABLE KEYS */;
INSERT INTO `doyen` VALUES (1,'misraoui','');
/*!40000 ALTER TABLE `doyen` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `emploi_du_temps`
--

DROP TABLE IF EXISTS `emploi_du_temps`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `emploi_du_temps` (
  `id` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `emploi_du_temps`
--

LOCK TABLES `emploi_du_temps` WRITE;
/*!40000 ALTER TABLE `emploi_du_temps` DISABLE KEYS */;
/*!40000 ALTER TABLE `emploi_du_temps` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `etudiant`
--

DROP TABLE IF EXISTS `etudiant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `etudiant` (
  `id_etudiant` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(50) DEFAULT NULL,
  `prenom` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_etudiant`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `etudiant`
--

LOCK TABLES `etudiant` WRITE;
/*!40000 ALTER TABLE `etudiant` DISABLE KEYS */;
INSERT INTO `etudiant` VALUES (1,'sabeur','sarah'),(2,'seghier','amine'),(3,'kaid','sirine');
/*!40000 ALTER TABLE `etudiant` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `professeur`
--

DROP TABLE IF EXISTS `professeur`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `professeur` (
  `id_prof` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(50) DEFAULT NULL,
  `prenom` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_prof`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `professeur`
--

LOCK TABLES `professeur` WRITE;
/*!40000 ALTER TABLE `professeur` DISABLE KEYS */;
INSERT INTO `professeur` VALUES (1,'belkacmi',''),(2,'amir',''),(3,'imam',''),(4,'djedai','');
/*!40000 ALTER TABLE `professeur` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(80) NOT NULL,
  `email` varchar(120) NOT NULL,
  `password` varchar(200) NOT NULL,
  `role` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-01-19 16:40:59
