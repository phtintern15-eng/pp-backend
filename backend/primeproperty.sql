-- MySQL dump 10.13  Distrib 8.0.46, for Win64 (x86_64)
--
-- Host: localhost    Database: primeproperty_v2
-- ------------------------------------------------------
-- Server version	8.0.46

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
-- Table structure for table `clients`
--

DROP TABLE IF EXISTS `clients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `clients` (
  `id` int NOT NULL AUTO_INCREMENT,
  `consultant_id` int NOT NULL,
  `first_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `client_type` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `notes` text COLLATE utf8mb4_unicode_ci,
  `created_at` datetime DEFAULT (now()),
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `consultant_id` (`consultant_id`),
  KEY `ix_clients_id` (`id`),
  CONSTRAINT `clients_ibfk_1` FOREIGN KEY (`consultant_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clients`
--

LOCK TABLES `clients` WRITE;
/*!40000 ALTER TABLE `clients` DISABLE KEYS */;
INSERT INTO `clients` VALUES (1,21,'ravi ','hr','ravihr12@gmail.com','7845122356','First-time Buyer','active','bangalore','2026-10-27 15:03:04',NULL);
/*!40000 ALTER TABLE `clients` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `consultant_profiles`
--

DROP TABLE IF EXISTS `consultant_profiles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `consultant_profiles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `license_number` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `years_experience` int DEFAULT NULL,
  `specialization` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `total_sales_volume` float DEFAULT NULL,
  `properties_sold` int DEFAULT NULL,
  `average_sale_price` float DEFAULT NULL,
  `client_satisfaction` float DEFAULT NULL,
  `primary_email` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `primary_phone` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `mobile_phone` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `fax_number` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `website` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `business_address` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `years_in_business` int DEFAULT NULL,
  `created_at` datetime DEFAULT (now()),
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  KEY `ix_consultant_profiles_id` (`id`),
  CONSTRAINT `consultant_profiles_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `consultant_profiles`
--

LOCK TABLES `consultant_profiles` WRITE;
/*!40000 ALTER TABLE `consultant_profiles` DISABLE KEYS */;
INSERT INTO `consultant_profiles` VALUES (1,4,'Not provided',0,'Not specified',0,0,0,0,'pht.intern15@gmail.com','8040480404','8040480404',NULL,NULL,NULL,0,'2026-10-13 09:48:56',NULL),(2,5,'Not provided',0,'Not specified',0,0,0,0,'pht.intern16@gmail.com','8040480404','8040480404',NULL,NULL,NULL,0,'2026-10-13 10:27:55',NULL),(3,6,'Not provided',0,'Not specified',0,0,0,0,'pht.intern18@gmail.com','8340480404','8340480404',NULL,NULL,NULL,0,'2026-10-13 10:45:50',NULL),(4,10,'Not provided',0,'Not specified',0,0,0,0,'nb14@gmail.com','7845121245','7845121245',NULL,NULL,NULL,0,'2026-10-14 11:01:28',NULL),(5,12,'Not provided',0,'Not specified',0,0,0,0,'pht.intern10@gmail.com','8340480404','8340480404',NULL,NULL,NULL,0,'2026-10-16 05:43:21',NULL),(6,14,'Not provided',0,'Not specified',0,0,0,0,'consultant_test@auraproperties.com',NULL,NULL,NULL,NULL,NULL,0,'2026-10-23 13:09:10',NULL),(7,19,'Not provided',0,'Not specified',0,0,0,0,'rajuhr18@gmail.com','8340480404','8340480404',NULL,NULL,NULL,0,'2026-10-26 15:51:05',NULL),(8,21,'Not provided',0,'Not specified',0,0,0,0,'pht.intern02@gmail.com','8040480404','8040480404',NULL,NULL,NULL,0,'2026-10-27 14:50:26',NULL);
/*!40000 ALTER TABLE `consultant_profiles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `consultation_requests`
--

DROP TABLE IF EXISTS `consultation_requests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `consultation_requests` (
  `id` int NOT NULL AUTO_INCREMENT,
  `consultant_id` int NOT NULL,
  `owner_id` int NOT NULL,
  `title` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `property_address` varchar(500) COLLATE utf8mb4_unicode_ci NOT NULL,
  `consultation_type` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text COLLATE utf8mb4_unicode_ci,
  `preferred_date` datetime DEFAULT NULL,
  `preferred_time` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `scheduled_date` datetime DEFAULT NULL,
  `scheduled_time` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `owner_name` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `owner_email` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `owner_phone` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` datetime DEFAULT (now()),
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `consultant_id` (`consultant_id`),
  KEY `owner_id` (`owner_id`),
  KEY `ix_consultation_requests_id` (`id`),
  CONSTRAINT `consultation_requests_ibfk_1` FOREIGN KEY (`consultant_id`) REFERENCES `users` (`id`),
  CONSTRAINT `consultation_requests_ibfk_2` FOREIGN KEY (`owner_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `consultation_requests`
--

LOCK TABLES `consultation_requests` WRITE;
/*!40000 ALTER TABLE `consultation_requests` DISABLE KEYS */;
/*!40000 ALTER TABLE `consultation_requests` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `consultations`
--

DROP TABLE IF EXISTS `consultations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `consultations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `first_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `company` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `property_count` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `property_types` text COLLATE utf8mb4_unicode_ci,
  `challenges` text COLLATE utf8mb4_unicode_ci,
  `features` text COLLATE utf8mb4_unicode_ci,
  `budget` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `timeline` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `current_software` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `team_size` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `preferred_contact` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `additional_info` text COLLATE utf8mb4_unicode_ci,
  `status` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` datetime DEFAULT (now()),
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `ix_consultations_id` (`id`),
  CONSTRAINT `consultations_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `consultations`
--

LOCK TABLES `consultations` WRITE;
/*!40000 ALTER TABLE `consultations` DISABLE KEYS */;
/*!40000 ALTER TABLE `consultations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `leads`
--

DROP TABLE IF EXISTS `leads`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `leads` (
  `id` int NOT NULL AUTO_INCREMENT,
  `consultant_id` int NOT NULL,
  `first_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `source` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `notes` text COLLATE utf8mb4_unicode_ci,
  `created_at` datetime DEFAULT (now()),
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `consultant_id` (`consultant_id`),
  KEY `ix_leads_id` (`id`),
  CONSTRAINT `leads_ibfk_1` FOREIGN KEY (`consultant_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `leads`
--

LOCK TABLES `leads` WRITE;
/*!40000 ALTER TABLE `leads` DISABLE KEYS */;
/*!40000 ALTER TABLE `leads` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `properties`
--

DROP TABLE IF EXISTS `properties`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `properties` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text COLLATE utf8mb4_unicode_ci,
  `address` varchar(500) COLLATE utf8mb4_unicode_ci NOT NULL,
  `city` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `state` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `zip_code` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `property_type` enum('RESIDENTIAL','COMMERCIAL','OFFICE') COLLATE utf8mb4_unicode_ci NOT NULL,
  `listing_type` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `bedrooms` int DEFAULT NULL,
  `bathrooms` int DEFAULT NULL,
  `area_sqft` float DEFAULT NULL,
  `price` float NOT NULL,
  `latitude` float DEFAULT NULL,
  `longitude` float DEFAULT NULL,
  `video_url` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `is_available` tinyint(1) DEFAULT NULL,
  `owner_id` int NOT NULL,
  `created_at` datetime DEFAULT (now()),
  `updated_at` datetime DEFAULT NULL,
  `foreign_buyer_eligible` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id`),
  KEY `owner_id` (`owner_id`),
  KEY `ix_properties_id` (`id`),
  CONSTRAINT `properties_ibfk_1` FOREIGN KEY (`owner_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=76 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `properties`
--

LOCK TABLES `properties` WRITE;
/*!40000 ALTER TABLE `properties` DISABLE KEYS */;
INSERT INTO `properties` VALUES (1,'The Bel-Air Glass Pavilion','An architectural tour de force featuring panoramic hillside vistas, zero-edge infinity pool, floor-to-ceiling motorized Fleetwood glass doors, and a custom Italian Poliform kitchen.','Beverly Hills, CA','Beverly Hills','CA','90210','RESIDENTIAL','sale',5,6,6400,4850000,NULL,NULL,NULL,1,1,'2026-10-12 11:07:30','2026-11-19 14:46:23',1),(2,'Skyline Horizon Penthouse','Perched high above Central Park, this duplex penthouse features a private wrap-around terrace, 14-foot ceilings, bespoke marble fireplaces, and unmatched skyline panoramas.','Manhattan, New York','Manhattan','New York','90210','RESIDENTIAL','sale',4,4,4950,6200000,NULL,NULL,NULL,1,1,'2026-10-12 11:07:30','2026-11-19 14:46:23',1),(3,'Azure Shoreline Ocean Villa','Private direct dockage with deepwater access, resort-style poolside cabanas, outdoor summer kitchen, and luminous open-plan living designed for ultimate seaside tranquility.','Miami Beach, FL','Miami Beach','FL','90210','RESIDENTIAL','sale',6,7,7100,5400000,NULL,NULL,NULL,1,1,'2026-10-12 11:07:30','2026-11-19 14:46:23',1),(4,'Nordic Minimalist Loft','Warm minimalist aesthetic with Scandinavian white oak floors, exposed architectural brick accents, custom fluted millwork, and top-tier Gaggenau appliances.','Tribeca, New York','Tribeca','New York','90210','RESIDENTIAL','rent',3,3,2850,14500,NULL,NULL,NULL,1,1,'2026-10-12 11:07:30','2026-11-19 14:46:23',1),(5,'The Aspen Ridge Chalet','Ski-in/ski-out luxury residence surrounded by evergreen forest. Highlights include heated stone terraces, indoor spa pool, floor-to-ceiling timber beams, and breathtaking mountain views.','Aspen, Colorado','Aspen','Colorado','90210','RESIDENTIAL','sale',5,5,5300,3950000,NULL,NULL,NULL,1,1,'2026-10-12 11:07:30','2026-11-19 14:46:23',1),(6,'The Metropolitan Oasis Residence','Contemporary urban luxury with a sprawling private botanical terrace, integrated Sub-Zero appliances, double rain showers, and 24-hour white-glove security.','Downtown Los Angeles, CA','Downtown Los Angeles','CA','90210','RESIDENTIAL','rent',3,3,3400,19000,NULL,NULL,NULL,1,1,'2026-10-12 11:07:30','2026-11-19 14:46:23',1),(7,'sukoon','1 bhk ','66th cross  1st stage  kumaraswamy layout ','bangalore','karnataka','560078','RESIDENTIAL','sale',1,0,500,9999.97,NULL,NULL,'https://www.youtube.com/watch?v=JO6vwIuXY3w',1,7,'2026-10-14 10:24:37',NULL,1),(8,'The Worli Ocean Penthouse','Triple-height duplex overlooking the Arabian Sea with private infinity pool and dedicated high-speed elevators.','Worli Mumbai','Worli Mumbai','IN','400001','RESIDENTIAL','Penthouse',5,4,8200,280000000,NULL,NULL,NULL,1,1,'2026-10-30 14:42:22',NULL,1),(9,'Pali Hill Portuguese Haven','Colonial heritage bungalow nestled inside prestigious leafy Pali Hill with manicured courtyards.','Bandra','Bandra','IN','400001','RESIDENTIAL','Heritage Estate',4,3,5500,180000000,NULL,NULL,NULL,1,1,'2026-10-30 14:42:22',NULL,1),(10,'Sanctuary of Palms Villa','Bespoke Balinese-Portuguese luxury villa surrounded by dense Goan greenery with private basalt pool.','Assagao Goa','Assagao Goa','IN','400001','RESIDENTIAL','Luxury Villa',4,3,6400,125000000,NULL,NULL,NULL,1,1,'2026-10-30 14:42:22',NULL,1),(11,'The Glade Mansions','Contemporary smart villa within a golf reserve featuring double-height glass facades and water features.','Whitefield Bengaluru','Whitefield Bengaluru','IN','400001','RESIDENTIAL','Luxury Villa',5,4,7100,89000000,NULL,NULL,NULL,1,1,'2026-10-30 14:42:22',NULL,1),(12,'Magnolia Sky Residence','Ultra-luxury golf course condominium with direct elevator access and concierge service.','Gurgaon NCR','Gurgaon NCR','IN','400001','RESIDENTIAL','Apartment',4,3,6200,142000000,NULL,NULL,NULL,1,1,'2026-10-30 14:42:22',NULL,1),(13,'Lutyens Imperial Pavilion','Exclusive sovereign estate in Delhi with sprawling private botanical lawns and diplomatic security.','Delhi NCR','Delhi NCR','IN','400001','RESIDENTIAL','Heritage Estate',6,5,11500,450000000,NULL,NULL,NULL,1,1,'2026-10-30 14:42:22',NULL,1),(14,'The Billionaire Frond Villa','Direct private beach access on Palm Jumeirah with panoramic views of the Dubai Marina skyline.','Palm Jumeirah','Palm Jumeirah','AE','400001','RESIDENTIAL','Luxury Villa',6,5,10800,22000000,NULL,NULL,NULL,1,1,'2026-10-30 14:42:22',NULL,1),(15,'Burj Crown Panoramic Sky Palace','Soaring penthouse directly facing Burj Khalifa with 360-degree wrapped terrace and spa salon.','Downtown Dubai','Downtown Dubai','AE','400001','RESIDENTIAL','Penthouse',4,3,6400,14500000,NULL,NULL,NULL,1,1,'2026-10-30 14:42:22',NULL,1),(16,'Emirates Hills Golf Manor','The Beverly Hills of Dubai. Bespoke neoclassical architecture overlooking the Montgomerie golf greens.','Emirates Hills','Emirates Hills','AE','400001','RESIDENTIAL','Luxury Villa',7,6,14000,26000000,NULL,NULL,NULL,1,1,'2026-10-30 14:42:22',NULL,1),(17,'Saadiyat Island Coral Pavilion','Eco-conscious beachfront sanctuary located adjacent to Louvre Abu Dhabi and cultural district.','Saadiyat Island','Saadiyat Island','AE','400001','RESIDENTIAL','Luxury Villa',5,4,7500,9800000,NULL,NULL,NULL,1,1,'2026-10-30 14:42:22',NULL,1),(18,'Marina Gate Skyline Suite','Full marina view designer apartment with private yacht mooring berth and health club.','Dubai Marina','Dubai Marina','AE','400001','RESIDENTIAL','Apartment',3,2,3800,7200000,NULL,NULL,NULL,1,1,'2026-10-30 14:42:22',NULL,1),(19,'Al Barari Royal Lagoon Retreat','Botanical oasis with botanical streams, private organic farm, and subterranean cinema.','Al Barari','Al Barari','AE','400001','RESIDENTIAL','Luxury Villa',5,4,8900,13900000,NULL,NULL,NULL,1,1,'2026-10-30 14:42:22',NULL,1),(20,'Bel Air Contemporary Atelier','Striking cantilevered glass architecture overlooking Los Angeles basin out to the Pacific Ocean.','California','California','US','400001','RESIDENTIAL','Luxury Villa',6,5,11200,24000000,NULL,NULL,NULL,1,1,'2026-10-30 14:42:22',NULL,1),(21,'Tribeca Cast Iron Triplex','Iconic cobblestone Tribeca loft with private rooftop heated pool, original beams, and wine cellar.','New York','New York','US','400001','RESIDENTIAL','Penthouse',4,3,6800,19500000,NULL,NULL,NULL,1,1,'2026-10-30 14:42:22',NULL,1),(22,'Star Island Waterfront Sanctuary','Miami ultra-prime deep-water frontage equipped for mega-yachts with resort-grade pool pavilion.','Florida','Florida','US','400001','RESIDENTIAL','Luxury Villa',7,6,12500,29000000,NULL,NULL,NULL,1,1,'2026-10-30 14:42:22',NULL,1),(23,'Lake Austin Modern Pavilion','Limestone and cedar lakefront sanctuary with private motorized boat dock and infinity pool.','Texas','Texas','US','400001','RESIDENTIAL','Luxury Villa',5,4,8400,11800000,NULL,NULL,NULL,1,1,'2026-10-30 14:42:22',NULL,1),(24,'Central Park West Classical Suite','Full park views from pre-war white-glove building with wood-burning fireplaces and library.','New York','New York','US','400001','RESIDENTIAL','Apartment',3,2,3600,8500000,NULL,NULL,NULL,1,1,'2026-10-30 14:42:22',NULL,1),(25,'Montecito Mediterranean Compound','Spanish colonial revival manor shaded by centenary olive trees and mountain views.','California','California','US','400001','RESIDENTIAL','Heritage Estate',5,4,7900,13500000,NULL,NULL,NULL,1,1,'2026-10-30 14:42:22',NULL,1),(26,'One Hyde Park Parkside Suite','Knightsbridge icon with Mandarin Oriental 24-hour room service, wine cellar, and private cinema.','London','London','UK','400001','RESIDENTIAL','Apartment',4,3,4800,18500000,NULL,NULL,NULL,1,1,'2026-10-30 14:42:22',NULL,1),(27,'Cotswolds Manor & Equestrian Stud','Grade-II listed honey-stone manor set on 45 rolling private acres with equestrian facilities.','Cotswolds','Cotswolds','UK','400001','RESIDENTIAL','Heritage Estate',7,6,10500,12000000,NULL,NULL,NULL,1,1,'2026-10-30 14:42:22',NULL,1),(28,'Cheyne Walk Riverside Mansion','Historic Georgian townhome facing River Thames with landscaped walled garden and private garage.','Chelsea','Chelsea','UK','400001','RESIDENTIAL','Heritage Estate',6,5,8200,21000000,NULL,NULL,NULL,1,1,'2026-10-30 14:42:22',NULL,1),(29,'Mayfair Mews House','Discreet cobblestone mews home renovated to museum-quality standards in heart of Mayfair.','London','London','UK','400001','RESIDENTIAL','Luxury Villa',3,2,3200,7900000,NULL,NULL,NULL,1,1,'2026-10-30 14:42:22',NULL,1),(30,'The Battersea Sky Penthouse','Direct Thames views perched atop iconic Battersea development with wrap-around glass terrace.','London','London','UK','400001','RESIDENTIAL','Penthouse',4,3,5100,14800000,NULL,NULL,NULL,1,1,'2026-10-30 14:42:22',NULL,1),(31,'Surrey Hills Wentworth Estate','Private gated golf compound with indoor pool, steam room, and direct access to fairway.','London','London','UK','400001','RESIDENTIAL','Luxury Villa',5,4,8000,9500000,NULL,NULL,NULL,1,1,'2026-10-30 14:42:22',NULL,1),(32,'The Bridle Path French Chateau','Limestone estate in Toronto Millionaires Row with indoor ballroom, indoor pool, and wine vault.','Toronto','Toronto','CA','400001','RESIDENTIAL','Heritage Estate',6,5,14500,17500000,NULL,NULL,NULL,1,1,'2026-10-30 14:42:22',NULL,1),(33,'West Vancouver Oceanfront Cliffhouse','Cantilevered architectural glass residence offering unobstructed views of English Bay.','Vancouver','Vancouver','CA','400001','RESIDENTIAL','Luxury Villa',5,4,7800,13800000,NULL,NULL,NULL,1,1,'2026-10-30 14:42:22',NULL,1),(34,'Yorkville Four Seasons Penthouse','Hotel-serviced penthouse in prime Yorkville with bespoke marble baths and 11-foot ceilings.','Toronto','Toronto','CA','400001','RESIDENTIAL','Penthouse',3,2,4200,8900000,NULL,NULL,NULL,1,1,'2026-10-30 14:42:22',NULL,1),(35,'Golden Square Mile Heritage Manor','Historic Mont-Royal stone mansion featuring hand-carved millwork and modern glass extension.','Montreal','Montreal','CA','400001','RESIDENTIAL','Heritage Estate',6,5,8200,7500000,NULL,NULL,NULL,1,1,'2026-10-30 14:42:22',NULL,1),(36,'Shaughnessy Classical Residence','First Shaughnessy estate set on expansive manicured grounds with heated stone driveway.','Vancouver','Vancouver','CA','400001','RESIDENTIAL','Luxury Villa',5,4,6900,11200000,NULL,NULL,NULL,1,1,'2026-10-30 14:42:22',NULL,1),(37,'Outremont Forest Villa','Serene contemporary estate integrated seamlessly into Mount Royal natural forestry.','Montreal','Montreal','CA','400001','RESIDENTIAL','Luxury Villa',4,3,5500,6800000,NULL,NULL,NULL,1,1,'2026-10-30 14:42:22',NULL,1),(38,'Point Piper Harbourfront Pavilion','Direct deep-water harbour frontage overlooking Sydney Harbour Bridge and Opera House.','Sydney','Sydney','AU','400001','RESIDENTIAL','Luxury Villa',5,4,9200,31000000,NULL,NULL,NULL,1,1,'2026-10-30 14:42:22',NULL,1),(39,'Toorak Georgian Botanical Manor','Prestigious Toorak cul-de-sac residence with tennis court, pavilion, and temperature cellar.','Melbourne','Melbourne','AU','400001','RESIDENTIAL','Heritage Estate',6,5,10000,14500000,NULL,NULL,NULL,1,1,'2026-10-30 14:42:22',NULL,1),(40,'Main Beach Oceanfront Penthouse','Uninterrupted Pacific Ocean panorama with private sky-deck pool and private boat berth.','Gold Coast','Gold Coast','AU','400001','RESIDENTIAL','Penthouse',4,3,6200,8800000,NULL,NULL,NULL,1,1,'2026-10-30 14:42:22',NULL,1),(41,'Darling Point Sky Residence','Bespoke European renovation overlooking yacht marina with private double garage.','Sydney','Sydney','AU','400001','RESIDENTIAL','Apartment',3,2,4100,12200000,NULL,NULL,NULL,1,1,'2026-10-30 14:42:22',NULL,1),(42,'South Yarra Minimalist Masterpiece','Architect-designed concrete and glass sculpture walking distance to Royal Botanic Gardens.','Melbourne','Melbourne','AU','400001','RESIDENTIAL','Luxury Villa',4,3,5800,9100000,NULL,NULL,NULL,1,1,'2026-10-30 14:42:22',NULL,1),(43,'Sovereign Islands Waterfront Haven','Guard-gated island estate engineered for superyacht mooring with 25-meter lap pool.','Gold Coast','Gold Coast','AU','400001','RESIDENTIAL','Luxury Villa',6,5,11000,16500000,NULL,NULL,NULL,1,1,'2026-10-30 14:42:22',NULL,1),(44,'Nassim Road Good Class Bungalow (GCB)','Singapores most prestigious embassy address set amidst dense private jungle and koi streams.','Nassim','Nassim','SG','400001','RESIDENTIAL','Luxury Villa',6,5,14000,35000000,NULL,NULL,NULL,1,1,'2026-10-30 14:42:22',NULL,1),(45,'Sentosa Cove Oceanfront Berth Villa','Only location in Singapore where foreign nationals can acquire titled luxury waterfront land.','Sentosa Cove','Sentosa Cove','SG','400001','RESIDENTIAL','Luxury Villa',5,4,8500,18200000,NULL,NULL,NULL,1,1,'2026-10-30 14:42:22',NULL,1),(46,'The Marq on Paterson Hill','Private 15-meter cantilevered lap pool built directly into the living room balcony.','Orchard','Orchard','SG','400001','RESIDENTIAL','Apartment',4,3,6300,13500000,NULL,NULL,NULL,1,1,'2026-10-30 14:42:22',NULL,1),(47,'Sculptura Ardmore Super Penthouse','Commanding top 3 floors of Ardmore Park with private sky gym, private garage elevator.','Orchard','Orchard','SG','400001','RESIDENTIAL','Penthouse',5,4,9200,24000000,NULL,NULL,NULL,1,1,'2026-10-30 14:42:22',NULL,1),(48,'Seven Palms Coral Villa','Low-rise beachfront condominium designed by Kerry Hill directly fronting South China Sea.','Sentosa Cove','Sentosa Cove','SG','400001','RESIDENTIAL','Apartment',3,2,4100,9500000,NULL,NULL,NULL,1,1,'2026-10-30 14:42:22',NULL,1),(49,'Cluny Hill Architectural Bungalow','Adjacent to Singapore Botanic Gardens (UNESCO Heritage) with geothermal cooling.','Nassim','Nassim','SG','400001','RESIDENTIAL','Luxury Villa',5,4,11000,28000000,NULL,NULL,NULL,1,1,'2026-10-30 14:42:22',NULL,1),(50,'Villa Bel Horizon Cap d\'Antibes','Legendary Belle Époque mansion with private Mediterranean sea access, helipad, and guest cottages.','French Riviera','French Riviera','FR','400001','RESIDENTIAL','Luxury Villa',7,6,9800,22500000,NULL,NULL,NULL,1,1,'2026-10-30 14:42:22','2026-11-12 12:06:25',1),(51,'Avenue Montaigne Haussmannian Jewel','Direct Eiffel Tower views in Golden Triangle featuring 19th-century gilt ceilings and parquet floors.','Paris','Paris','FR','400001','RESIDENTIAL','Apartment',4,3,4900,12800000,NULL,NULL,NULL,1,1,'2026-10-30 14:42:22',NULL,1),(52,'Les Parcs de Saint-Tropez Waterfront','Ultra-exclusive private domain in Saint-Tropez with 24/7 armed security and private mooring.','Saint-Tropez','Saint-Tropez','FR','400001','RESIDENTIAL','Luxury Villa',6,5,8500,26000000,NULL,NULL,NULL,1,1,'2026-10-30 14:42:22',NULL,1),(53,'Place des Vosges Heritage Hôtel Particulier','17th-century private mansion in Paris oldest planned square with private courtyard.','Paris','Paris','FR','400001','RESIDENTIAL','Heritage Estate',5,4,6200,16500000,NULL,NULL,NULL,1,1,'2026-10-30 14:42:22',NULL,1),(54,'Cannes Croisette Sky Terrace','Frontline panoramic sea views overlooking the Palais des Festivals with private rooftop jacuzzi.','French Riviera','French Riviera','FR','400001','RESIDENTIAL','Penthouse',3,2,3800,8500000,NULL,NULL,NULL,1,1,'2026-10-30 14:42:22',NULL,1),(55,'Ramatuelle Pine Forest Bastide','Authentic stone country estate overlooking Pampelonne Beach with olive groves.','Saint-Tropez','Saint-Tropez','FR','400001','RESIDENTIAL','Luxury Villa',5,4,5900,9800000,NULL,NULL,NULL,1,1,'2026-10-30 14:42:22',NULL,1),(56,'Lake Starnberg Grand Shore Estate','Rare private lakefront access on Lake Starnberg with private boathouse and Alpine vistas.','Lake Starnberg','Lake Starnberg','DE','400001','RESIDENTIAL','Heritage Estate',7,6,12000,18000000,NULL,NULL,NULL,1,1,'2026-10-30 14:42:22',NULL,1),(57,'Bogenhausen Bauhaus Villa','Munich premier diplomatic quarter. Architectural villa with geothermal energy and indoor pool.','Munich','Munich','DE','400001','RESIDENTIAL','Luxury Villa',5,4,7500,12500000,NULL,NULL,NULL,1,1,'2026-10-30 14:42:22',NULL,1),(58,'Grunewald Forest Diplomatic Residence','Peaceful villa in Berlins historic billionaire forest with secure gated motor court.','Berlin','Berlin','DE','400001','RESIDENTIAL','Luxury Villa',6,5,8400,9200000,NULL,NULL,NULL,1,1,'2026-10-30 14:42:22',NULL,1),(59,'Mitte Industrial Rooftop Penthouse','Dramatic loft penthouse with 360-degree Berlin TV Tower views and private elevator.','Berlin','Berlin','DE','400001','RESIDENTIAL','Penthouse',3,2,4600,6800000,NULL,NULL,NULL,1,1,'2026-10-30 14:42:22',NULL,1),(60,'Nymphenburg Canal Palace Residence','Historic villa directly overlooking the royal palace canal with protected private parklands.','Munich','Munich','DE','400001','RESIDENTIAL','Heritage Estate',5,4,9100,14800000,NULL,NULL,NULL,1,1,'2026-10-30 14:42:22',NULL,1),(61,'Tutzing Alpine Panorama Villa','Contemporary eco-mansion with floor-to-ceiling glass capturing both lake and Zugspitze peak.','Lake Starnberg','Lake Starnberg','DE','400001','RESIDENTIAL','Luxury Villa',5,4,6800,11500000,NULL,NULL,NULL,1,1,'2026-10-30 14:42:22',NULL,1),(62,'Cologny Waterfront Estate','Prestigious Cologny hillside overlooking Lake Geneva and the Jet d\\','Geneva','Geneva','CH','400001','RESIDENTIAL','Luxury Villa',6,5,11000,28000000,NULL,NULL,NULL,1,1,'2026-10-30 14:42:22',NULL,1),(63,'Zürichberg Gold Coast Pavilion','High above Zurich city with panorama of Lake Zurich, infinity pool, and underground 6-car gallery.','Zurich','Zurich','CH','400001','RESIDENTIAL','Luxury Villa',5,4,7800,15800000,NULL,NULL,NULL,1,1,'2026-10-30 14:42:22',NULL,1),(64,'Old Town Geneva Duplex Penthouse','Exquisitely preserved historic beamed residence minutes from banking district and luxury boutiques.','Geneva','Geneva','CH','400001','RESIDENTIAL','Penthouse',4,3,4800,9800000,NULL,NULL,NULL,1,1,'2026-10-30 14:42:22',NULL,1),(65,'Suvretta Hill Top Residence','Situated on the Suvretta corridor with direct ski access and private pine forest.','St. Moritz','St. Moritz','CH','400001','RESIDENTIAL','Luxury Villa',5,4,6900,14000000,NULL,NULL,NULL,1,1,'2026-10-30 14:42:22',NULL,1),(66,'Küsnacht Lakefront Villa','Prime Zurich Gold Coast address with private stone pier, sauna, and sun terrace.','Zurich','Zurich','CH','400001','RESIDENTIAL','Luxury Villa',4,3,5500,11200000,NULL,NULL,NULL,1,1,'2026-10-30 14:42:22',NULL,1),(67,'Minami-Aoyama Glass Sanctuary','Custom contemporary freestanding residence in Tokyo fashion capital with private bamboo courtyard.','Tokyo','Tokyo','JP','400001','RESIDENTIAL','Luxury Villa',4,3,6200,1650000,NULL,NULL,NULL,1,1,'2026-10-30 14:42:22',NULL,1),(68,'Niseko Hanazono Ski Chalet','Ski-in ski-out modern timber masterpiece with natural onsen hot spring bath and Mount Yotei views.','Niseko','Niseko','JP','400001','RESIDENTIAL','Luxury Villa',5,4,7400,1200000,NULL,NULL,NULL,1,1,'2026-10-30 14:42:22',NULL,1),(69,'Higashiyama Heritage Sukiya Estate','Century-old restored master estate adjacent to Nanzen-ji temple with cascading stream garden.','Kyoto','Kyoto','JP','400001','RESIDENTIAL','Heritage Estate',5,4,8000,1450000,NULL,NULL,NULL,1,1,'2026-10-30 14:42:22',NULL,1),(70,'Toranomon Hills Tower Penthouse','Soaring over Tokyo Tower with Hyatt Andaz luxury hotel services and private sky lounge.','Tokyo','Tokyo','JP','400001','RESIDENTIAL','Penthouse',4,3,5500,2200000,NULL,NULL,NULL,1,1,'2026-10-30 14:42:22',NULL,1),(71,'Kamo River View Kyoto Residence','Rare frontline view of Kamo River and Higashiyama mountains with Hinoki wood baths.','Kyoto','Kyoto','JP','400001','RESIDENTIAL','Apartment',3,2,3400,780000,NULL,NULL,NULL,1,1,'2026-10-30 14:42:22',NULL,1),(72,'Hirafu Grand Lodge','Expansive private ski lodge walking distance to Hirafu gondola with outdoor stone onsen.','Niseko','Niseko','JP','400001','RESIDENTIAL','Luxury Villa',4,3,5000,890000,NULL,NULL,NULL,1,1,'2026-10-30 14:42:22',NULL,1),(73,'ayush',' 2bhk  rent house  ',' 10 th cross isro layout  Bangalore ','bangalore','karnataka','560078','RESIDENTIAL','rent',2,2,65000,20000,NULL,NULL,NULL,1,23,'2026-11-04 16:25:41',NULL,1),(74,'chinmayi','2 bhk rented house ',' 10 th cross isro layout  Bengalore ','bangalore','karnataka','560078','RESIDENTIAL','rent',2,2,5000,20000,NULL,NULL,NULL,1,25,'2026-11-04 16:58:24',NULL,0),(75,'Badrutt\'s Way Alpine Chalet','Exclusive ski-in ski-out timber and stone chalet with wellness spa, heated indoor pool, and ski lounge.','Via Serlas 27, 7500 St. Moritz','St. Moritz','Graubünden','7500','RESIDENTIAL','sale',7,8,9500,24500000,NULL,NULL,NULL,1,1,'2026-11-12 12:06:25',NULL,1);
/*!40000 ALTER TABLE `properties` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `property_images`
--

DROP TABLE IF EXISTS `property_images`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `property_images` (
  `id` int NOT NULL AUTO_INCREMENT,
  `property_id` int NOT NULL,
  `image_url` varchar(500) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_primary` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT (now()),
  PRIMARY KEY (`id`),
  KEY `property_id` (`property_id`),
  KEY `ix_property_images_id` (`id`),
  CONSTRAINT `property_images_ibfk_1` FOREIGN KEY (`property_id`) REFERENCES `properties` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=74 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `property_images`
--

LOCK TABLES `property_images` WRITE;
/*!40000 ALTER TABLE `property_images` DISABLE KEYS */;
INSERT INTO `property_images` VALUES (1,1,'/static/images/hero_luxury_villa.jpg',1,'2026-10-12 11:07:30'),(2,2,'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=1200&q=80',1,'2026-10-12 11:07:30'),(3,3,'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80',1,'2026-10-12 11:07:30'),(4,4,'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1200&q=80',1,'2026-10-12 11:07:30'),(5,5,'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=1200&q=80',1,'2026-10-12 11:07:30'),(6,6,'https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?auto=format&fit=crop&w=1200&q=80',1,'2026-10-12 11:07:30'),(7,7,'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQwvvvJTsdjKfjSEQ8STJv_8YgqsgkFM_oQ3COO5ZbhHw&s=10',1,'2026-10-14 10:41:00'),(8,8,'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80',1,'2026-10-30 14:42:22'),(9,9,'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1200&q=80',1,'2026-10-30 14:42:22'),(10,10,'https://images.unsplash.com/photo-1613977257363-707ba9348227?auto=format&fit=crop&w=1200&q=80',1,'2026-10-30 14:42:22'),(11,11,'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=1200&q=80',1,'2026-10-30 14:42:22'),(12,12,'https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?auto=format&fit=crop&w=1200&q=80',1,'2026-10-30 14:42:22'),(13,13,'https://images.unsplash.com/photo-1580587771525-78b9dba3b914?auto=format&fit=crop&w=1200&q=80',1,'2026-10-30 14:42:22'),(14,14,'https://images.unsplash.com/photo-1512915922686-57c11dde9b6b?auto=format&fit=crop&w=1200&q=80',1,'2026-10-30 14:42:22'),(15,15,'https://images.unsplash.com/photo-1567496898669-ee935f5f647a?auto=format&fit=crop&w=1200&q=80',1,'2026-10-30 14:42:22'),(16,16,'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=1200&q=80',1,'2026-10-30 14:42:22'),(17,17,'https://images.unsplash.com/photo-1613490493576-7fde63acd811?auto=format&fit=crop&w=1200&q=80',1,'2026-10-30 14:42:22'),(18,18,'https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?auto=format&fit=crop&w=1200&q=80',1,'2026-10-30 14:42:22'),(19,19,'https://images.unsplash.com/photo-1600607687920-4e2a09cf159d?auto=format&fit=crop&w=1200&q=80',1,'2026-10-30 14:42:22'),(20,20,'https://images.unsplash.com/photo-1600585154526-990dced4db0d?auto=format&fit=crop&w=1200&q=80',1,'2026-10-30 14:42:22'),(21,21,'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?auto=format&fit=crop&w=1200&q=80',1,'2026-10-30 14:42:22'),(22,22,'https://images.unsplash.com/photo-1580587771525-78b9dba3b914?auto=format&fit=crop&w=1200&q=80',1,'2026-10-30 14:42:22'),(23,23,'https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?auto=format&fit=crop&w=1200&q=80',1,'2026-10-30 14:42:22'),(24,24,'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?auto=format&fit=crop&w=1200&q=80',1,'2026-10-30 14:42:22'),(25,25,'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=1200&q=80',1,'2026-10-30 14:42:22'),(26,26,'https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?auto=format&fit=crop&w=1200&q=80',1,'2026-10-30 14:42:22'),(27,27,'https://images.unsplash.com/photo-1580587771525-78b9dba3b914?auto=format&fit=crop&w=1200&q=80',1,'2026-10-30 14:42:22'),(28,28,'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1200&q=80',1,'2026-10-30 14:42:22'),(29,29,'https://images.unsplash.com/photo-1600607687920-4e2a09cf159d?auto=format&fit=crop&w=1200&q=80',1,'2026-10-30 14:42:22'),(30,30,'https://images.unsplash.com/photo-1567496898669-ee935f5f647a?auto=format&fit=crop&w=1200&q=80',1,'2026-10-30 14:42:22'),(31,31,'https://images.unsplash.com/photo-1613977257363-707ba9348227?auto=format&fit=crop&w=1200&q=80',1,'2026-10-30 14:42:22'),(32,32,'https://images.unsplash.com/photo-1580587771525-78b9dba3b914?auto=format&fit=crop&w=1200&q=80',1,'2026-10-30 14:42:22'),(33,33,'https://images.unsplash.com/photo-1600585154526-990dced4db0d?auto=format&fit=crop&w=1200&q=80',1,'2026-10-30 14:42:22'),(34,34,'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80',1,'2026-10-30 14:42:22'),(35,35,'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1200&q=80',1,'2026-10-30 14:42:22'),(36,36,'https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?auto=format&fit=crop&w=1200&q=80',1,'2026-10-30 14:42:22'),(37,37,'https://images.unsplash.com/photo-1613977257363-707ba9348227?auto=format&fit=crop&w=1200&q=80',1,'2026-10-30 14:42:22'),(38,38,'https://images.unsplash.com/photo-1512915922686-57c11dde9b6b?auto=format&fit=crop&w=1200&q=80',1,'2026-10-30 14:42:22'),(39,39,'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1200&q=80',1,'2026-10-30 14:42:22'),(40,40,'https://images.unsplash.com/photo-1567496898669-ee935f5f647a?auto=format&fit=crop&w=1200&q=80',1,'2026-10-30 14:42:22'),(41,41,'https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?auto=format&fit=crop&w=1200&q=80',1,'2026-10-30 14:42:22'),(42,42,'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=1200&q=80',1,'2026-10-30 14:42:22'),(43,43,'https://images.unsplash.com/photo-1613490493576-7fde63acd811?auto=format&fit=crop&w=1200&q=80',1,'2026-10-30 14:42:22'),(44,44,'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=1200&q=80',1,'2026-10-30 14:42:22'),(45,45,'https://images.unsplash.com/photo-1512915922686-57c11dde9b6b?auto=format&fit=crop&w=1200&q=80',1,'2026-10-30 14:42:22'),(46,46,'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?auto=format&fit=crop&w=1200&q=80',1,'2026-10-30 14:42:22'),(47,47,'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80',1,'2026-10-30 14:42:22'),(48,48,'https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?auto=format&fit=crop&w=1200&q=80',1,'2026-10-30 14:42:22'),(49,49,'https://images.unsplash.com/photo-1600585154526-990dced4db0d?auto=format&fit=crop&w=1200&q=80',1,'2026-10-30 14:42:22'),(50,50,'https://images.unsplash.com/photo-1613977257363-707ba9348227?auto=format&fit=crop&w=1200&q=80',1,'2026-10-30 14:42:22'),(51,51,'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?auto=format&fit=crop&w=1200&q=80',1,'2026-10-30 14:42:22'),(52,52,'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=1200&q=80',1,'2026-10-30 14:42:22'),(53,53,'https://images.unsplash.com/photo-1580587771525-78b9dba3b914?auto=format&fit=crop&w=1200&q=80',1,'2026-10-30 14:42:22'),(54,54,'https://images.unsplash.com/photo-1567496898669-ee935f5f647a?auto=format&fit=crop&w=1200&q=80',1,'2026-10-30 14:42:22'),(55,55,'https://images.unsplash.com/photo-1600607687920-4e2a09cf159d?auto=format&fit=crop&w=1200&q=80',1,'2026-10-30 14:42:22'),(56,56,'https://images.unsplash.com/photo-1580587771525-78b9dba3b914?auto=format&fit=crop&w=1200&q=80',1,'2026-10-30 14:42:22'),(57,57,'https://images.unsplash.com/photo-1600585154526-990dced4db0d?auto=format&fit=crop&w=1200&q=80',1,'2026-10-30 14:42:22'),(58,58,'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=1200&q=80',1,'2026-10-30 14:42:22'),(59,59,'https://images.unsplash.com/photo-1567496898669-ee935f5f647a?auto=format&fit=crop&w=1200&q=80',1,'2026-10-30 14:42:22'),(60,60,'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1200&q=80',1,'2026-10-30 14:42:22'),(61,61,'https://images.unsplash.com/photo-1613977257363-707ba9348227?auto=format&fit=crop&w=1200&q=80',1,'2026-10-30 14:42:22'),(62,62,'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=1200&q=80',1,'2026-10-30 14:42:22'),(63,63,'https://images.unsplash.com/photo-1600585154526-990dced4db0d?auto=format&fit=crop&w=1200&q=80',1,'2026-10-30 14:42:22'),(64,64,'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80',1,'2026-10-30 14:42:22'),(65,65,'https://images.unsplash.com/photo-1613977257363-707ba9348227?auto=format&fit=crop&w=1200&q=80',1,'2026-10-30 14:42:22'),(66,66,'https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?auto=format&fit=crop&w=1200&q=80',1,'2026-10-30 14:42:22'),(67,67,'https://images.unsplash.com/photo-1600585154526-990dced4db0d?auto=format&fit=crop&w=1200&q=80',1,'2026-10-30 14:42:22'),(68,68,'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=1200&q=80',1,'2026-10-30 14:42:22'),(69,69,'https://images.unsplash.com/photo-1580587771525-78b9dba3b914?auto=format&fit=crop&w=1200&q=80',1,'2026-10-30 14:42:22'),(70,70,'https://images.unsplash.com/photo-1567496898669-ee935f5f647a?auto=format&fit=crop&w=1200&q=80',1,'2026-10-30 14:42:22'),(71,71,'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?auto=format&fit=crop&w=1200&q=80',1,'2026-10-30 14:42:22'),(72,72,'https://images.unsplash.com/photo-1613977257363-707ba9348227?auto=format&fit=crop&w=1200&q=80',1,'2026-10-30 14:42:22'),(73,75,'https://images.unsplash.com/photo-1580587771525-78b9dba3b914?auto=format&fit=crop&w=1200&q=80',1,'2026-11-12 12:06:25');
/*!40000 ALTER TABLE `property_images` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `service_requests`
--

DROP TABLE IF EXISTS `service_requests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `service_requests` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `service_type` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `property_id` int DEFAULT NULL,
  `description` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `urgency` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `scheduled_date` datetime DEFAULT NULL,
  `created_at` datetime DEFAULT (now()),
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `property_id` (`property_id`),
  KEY `ix_service_requests_id` (`id`),
  CONSTRAINT `service_requests_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `service_requests_ibfk_2` FOREIGN KEY (`property_id`) REFERENCES `properties` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `service_requests`
--

LOCK TABLES `service_requests` WRITE;
/*!40000 ALTER TABLE `service_requests` DISABLE KEYS */;
/*!40000 ALTER TABLE `service_requests` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `services`
--

DROP TABLE IF EXISTS `services`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `services` (
  `id` int NOT NULL AUTO_INCREMENT,
  `consultant_id` int NOT NULL,
  `service_name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text COLLATE utf8mb4_unicode_ci,
  `service_rate` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT (now()),
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `consultant_id` (`consultant_id`),
  KEY `ix_services_id` (`id`),
  CONSTRAINT `services_ibfk_1` FOREIGN KEY (`consultant_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `services`
--

LOCK TABLES `services` WRITE;
/*!40000 ALTER TABLE `services` DISABLE KEYS */;
/*!40000 ALTER TABLE `services` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_sessions`
--

DROP TABLE IF EXISTS `user_sessions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_sessions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `session_token` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ip_address` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `user_agent` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `expires_at` datetime NOT NULL,
  `created_at` datetime DEFAULT (now()),
  `is_active` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_user_sessions_session_token` (`session_token`),
  KEY `user_id` (`user_id`),
  KEY `ix_user_sessions_id` (`id`),
  CONSTRAINT `user_sessions_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_sessions`
--

LOCK TABLES `user_sessions` WRITE;
/*!40000 ALTER TABLE `user_sessions` DISABLE KEYS */;
INSERT INTO `user_sessions` VALUES (1,1,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbkBwcmltZXByb3BlcnRpZXMuY29tIiwiZXhwIjoxNzkzOTYyMTE5fQ.Vj0frNoyicL4-uOTxymeAb78AIuUToEFTguooi-Sz4Y','127.0.0.1','Werkzeug/2.3.8','2026-11-06 10:48:39','2026-11-06 15:48:39',0),(2,1,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbkBwcmltZXByb3BlcnRpZXMuY29tIiwiZXhwIjoxNzkzOTYyMjI5fQ.em7dkiDqtOcx3l9JzPJKrSsm_h6R3yESd8UmSpASivk','127.0.0.1','Werkzeug/2.3.8','2026-11-06 10:50:29','2026-11-06 15:50:29',0),(3,1,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbkBwcmltZXByb3BlcnRpZXMuY29tIiwiZXhwIjoxNzkzOTY0MTY2fQ.NLmweTDVEZ6o2fPepturSXgR4s8bnOrQs6Rp4hcCiDg','127.0.0.1','Werkzeug/2.3.8','2026-11-06 11:22:47','2026-11-06 16:22:46',0),(4,4,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJwaHQuaW50ZXJuMTVAZ21haWwuY29tIiwiZXhwIjoxNzkzOTY0OTQ4fQ.L8cqZXoV1cQ4BZSBqEfSGC6mF9uv6X8jsbwdbL2pC7s','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/157.0.0.0 Safari/537.36','2026-11-06 11:35:48','2026-11-06 16:35:48',0),(5,4,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJwaHQuaW50ZXJuMTVAZ21haWwuY29tIiwiZXhwIjoxNzk0NDYzNDU4fQ.jSTOgUWy455mfusevs84FF6KqFOkW4RDalMhFj53hiU','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/157.0.0.0 Safari/537.36','2026-11-12 06:04:19','2026-11-12 11:04:18',0),(6,4,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJwaHQuaW50ZXJuMTVAZ21haWwuY29tIiwiZXhwIjoxNzk0NDY0MTY0fQ.SXJEMe8Ua3ZearuDjp5_O8ZF6aEtVb_wvVDkE6gvoK0','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/157.0.0.0 Safari/537.36','2026-11-12 06:16:04','2026-11-12 11:16:04',0),(7,4,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJwaHQuaW50ZXJuMTVAZ21haWwuY29tIiwiZXhwIjoxNzk0NDc2ODQzfQ.9In3WStxMUE4I2xczKf1ptE6GLFI4zUMKyyu3eKusrA','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/157.0.0.0 Safari/537.36','2026-11-12 09:47:24','2026-11-12 14:47:23',0),(8,1,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbkBwcmltZXByb3BlcnRpZXMuY29tIiwiZXhwIjoxNzk0ODI1OTU2fQ.5SzMSwrRkYos3Zdb6jrvSpi1PG5ZBjIKmKPvwxzKgRE','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/157.0.0.0 Safari/537.36','2026-11-16 10:45:57','2026-11-16 15:45:56',0),(9,1,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbkBwcmltZXByb3BlcnRpZXMuY29tIiwiZXhwIjoxNzk0ODI3ODU1fQ.KHHOCMbyHJB8JQLM2BeCxeN2aq6VciMG5VSjW4XQyEY','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/157.0.0.0 Safari/537.36','2026-11-16 11:17:36','2026-11-16 16:17:35',0),(10,1,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbkBwcmltZXByb3BlcnRpZXMuY29tIiwiZXhwIjoxNzk0ODI5OTMxfQ.e61HZ12hckyBO5YGbSqqsTNq9v-0poq2CepS7SP2ycM','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/157.0.0.0 Safari/537.36','2026-11-16 11:52:11','2026-11-16 16:52:11',0),(11,1,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbkBwcmltZXByb3BlcnRpZXMuY29tIiwiZXhwIjoxNzk0ODMwODI3fQ.VxHrUiLm73JpC0cc0AASsc6LAjl1l3KoVE8hUH7uCso','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/157.0.0.0 Safari/537.36','2026-11-16 12:07:07','2026-11-16 17:07:07',0),(12,1,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbkBwcmltZXByb3BlcnRpZXMuY29tIiwiZXhwIjoxNzk0OTA3NzMzfQ.cE2qjngBbt-lPeKu4dly2CSZziWa6R9MmOs22uAEPpw','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/157.0.0.0 Safari/537.36','2026-11-17 09:28:53','2026-11-17 14:28:53',0),(13,1,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbkBwcmltZXByb3BlcnRpZXMuY29tIiwiZXhwIjoxNzk0OTA5NTg5fQ.0v7hqfLM0R7gg_LDnKHMECqdG369ED27rPl6rtMcQh0','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/157.0.0.0 Safari/537.36','2026-11-17 09:59:50','2026-11-17 14:59:49',0),(14,1,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbkBwcmltZXByb3BlcnRpZXMuY29tIiwiZXhwIjoxNzk0OTEwNjU1fQ.VWkkfgjxhOESyyuYu3uEdkheKpDMF0L-8bEd8k2sv7E','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/157.0.0.0 Safari/537.36','2026-11-17 10:17:35','2026-11-17 15:17:35',1),(15,1,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbkBwcmltZXByb3BlcnRpZXMuY29tIiwiZXhwIjoxNzk0OTEzMzU3fQ.2zoPovfZEKzmV-k5MDHQdBrRor2jnp7OjCz97DQOUsk','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/157.0.0.0 Safari/537.36','2026-11-17 11:02:37','2026-11-17 16:02:37',1),(16,1,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbkBwcmltZXByb3BlcnRpZXMuY29tIiwiZXhwIjoxNzk0OTk3NTEyfQ.r1IGnuKnu1pDyRll3SLu0Ds4_IyxQ-R1WkWGQOY4LdY','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/157.0.0.0 Safari/537.36','2026-11-18 10:25:13','2026-11-18 15:25:12',1),(17,1,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbkBwcmltZXByb3BlcnRpZXMuY29tIiwiZXhwIjoxNzk1MDc0NjcxfQ.1P5w2CkWZc0OAYnPv2AjoAvY70JemTbIUQgYPuxI4Es','127.0.0.1','Werkzeug/2.3.8','2026-11-19 07:51:12','2026-11-19 12:51:11',1),(18,1,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbkBwcmltZXByb3BlcnRpZXMuY29tIiwiZXhwIjoxNzk1MTU5NjI2fQ.2vbULCTOuTNC__LdkOfmo_4l9fUTIs3ouQyQWNZyFdM','127.0.0.1','Werkzeug/2.3.8','2026-11-20 07:27:07','2026-11-19 12:57:06',1);
/*!40000 ALTER TABLE `user_sessions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `hashed_password` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `user_type` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `company` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `property_count` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `location` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `subscription_plan` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `latitude` float DEFAULT NULL,
  `longitude` float DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  `is_admin` tinyint(1) DEFAULT NULL,
  `profile_image` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` datetime DEFAULT (now()),
  `updated_at` datetime DEFAULT NULL,
  `citizenship_status` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `residence_country` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `target_purchase_country` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_users_email` (`email`),
  KEY `ix_users_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin@primeproperties.com','Admin','Prime',NULL,'$2b$12$juz4ljMVhtut0vb1molE9..t8nWPUx5zr2Gg3SDmMLxedlt1OGqEe','admin','Prime Properties',NULL,'New York',NULL,NULL,NULL,1,1,NULL,'2026-10-12 11:07:30',NULL,NULL,NULL,NULL),(3,'testuser_new@example.com','Test','User',NULL,'$2b$12$0dPlSIXrtTykpS3t.AXKOuyrCGHUJRL1GWsNMQVvAg.k9aD9v/wAi','owner',NULL,NULL,NULL,NULL,NULL,NULL,1,0,NULL,'2026-10-13 09:48:07',NULL,NULL,NULL,NULL),(4,'pht.intern15@gmail.com','Pht','Intern15','8040480404','$2b$12$PNq.h1WAnBY48W0nJQJGrOORcX5hmi1APWwZ03AYKaMPN1LRE1IwC','admin',NULL,NULL,NULL,NULL,NULL,NULL,1,1,NULL,'2026-10-13 09:48:46',NULL,NULL,NULL,NULL),(5,'pht.intern16@gmail.com','Pht','Intern15','8040480404','$2b$12$pTtd0avL4n9/65ezYWDAMuzmpDCHEnnBwtTfuRvO3QzI.mt0Y0ri6','consultant',NULL,NULL,NULL,NULL,NULL,NULL,1,0,NULL,'2026-10-13 10:27:43',NULL,NULL,NULL,NULL),(6,'pht.intern18@gmail.com','Pht','Intern15','8340480404','$2b$12$9pHaxCKY40HqRbDroy1lpeksJ8jnuHsV2JTP7rTTOVGUXDrKGwIFe','consultant',NULL,NULL,'bangalore',NULL,NULL,NULL,1,0,NULL,'2026-10-13 10:45:37','2026-10-13 11:49:55',NULL,NULL,NULL),(7,'pht.intern12@gmail.com','Pht','Intern15','7845122356','$2b$12$p02DoL5spb7LWyBFbL0To.UjKIG3.GsrrVVqzyeKLOxXrv5ApH0..','owner','property','6-20',NULL,'Executive',NULL,NULL,1,0,'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D','2026-10-13 10:47:30','2026-10-14 10:17:29',NULL,NULL,NULL),(8,'test_reg_probe@example.com','Test','User',NULL,'$2b$12$wyiGqGLqYL1kxmD9fda01eE5TqqKubAZeZYWJCXtv7rjJTajEgX7y','consultant',NULL,NULL,NULL,NULL,NULL,NULL,1,0,NULL,'2026-10-13 11:29:42',NULL,NULL,NULL,NULL),(9,'consultant_ae2baf@test.com','Alexander','Vance','+1 555-0199','$2b$12$FO7TupeDAC6XdZ5WEAKkVO.DYxOTOVeYa5cbWap/ncFyjQX.iulbG','consultant',NULL,NULL,NULL,NULL,NULL,NULL,1,0,NULL,'2026-10-13 11:38:06',NULL,NULL,NULL,NULL),(10,'nb14@gmail.com','n','b','7845121245','$2b$12$iclI8bSRvvKjxXCLyINoO.cnbty2uTTunnblWZLzNKlhxHa4nW.vy','consultant',NULL,NULL,NULL,NULL,NULL,NULL,1,0,NULL,'2026-10-14 11:00:45',NULL,NULL,NULL,NULL),(11,'pht.intern17@gmail.com','Pht','Intern15','6965959475','$2b$12$CmdEidyciUb/x9u/Kp7ZuO7VB66gAqN2B9lkr.CN2abSAy6tjPKl2','owner','property','1-5','banhalore','Executive',NULL,NULL,1,0,NULL,'2026-10-14 11:08:12',NULL,NULL,NULL,NULL),(12,'pht.intern10@gmail.com','Pht','Intern15','8340480404','$2b$12$QvlvxeIywzGKV5awCy.eSuFx09fbfroI/UdTuhemjTiiZIj1vb6Hi','consultant',NULL,NULL,NULL,NULL,NULL,NULL,1,0,NULL,'2026-10-16 05:43:13',NULL,NULL,NULL,NULL),(13,'nbhs18@gmail.com','nb','hs','6965959475','$2b$12$3HsT3Yqd89UdoRSF60SDDOR7Hk9roUPeKCF5B/RdlNSXKcseKQdSi','owner','the property','1-5','banhalore','Presidential',NULL,NULL,1,0,NULL,'2026-10-23 13:01:06',NULL,NULL,NULL,NULL),(14,'consultant_test@auraproperties.com','Alexander','Vance',NULL,'$2b$12$GvS/QlWS.aocxhPFjLYcguSkWojabadnPyoKVxtas44rF3jqwNp7.','consultant',NULL,NULL,NULL,NULL,NULL,NULL,1,0,NULL,'2026-10-23 13:08:47',NULL,NULL,NULL,NULL),(17,'buyer_test_remote@example.com','Test','Buyer','+123456789','$2b$12$cDgq.OLSoGBuK17/liZhg.C0oKwwTOhgG2tQIOU.IWUHYUDzoFHd.','buyer',NULL,NULL,NULL,NULL,NULL,NULL,1,0,NULL,'2026-10-26 14:14:13',NULL,'nri','United States of America','India'),(18,'ravihi15@gamil.com','ravi','hi','7845122356','$2b$12$vvI4Vkm6B4ZBTPBFO0SSQemVVxq7anqeE/SBsBPASustVq6MA2P96','owner','property','1-5','banhalore','Executive',NULL,NULL,1,0,NULL,'2026-10-26 14:48:45',NULL,'nri','United States','India'),(19,'rajuhr18@gmail.com','raju','hr','8340480404','$2b$12$1xFD5zIPF4nr3IaPHscGzuWszPC5t7b.PykfGmo1MymTxoRb9I58S','consultant',NULL,NULL,NULL,NULL,NULL,NULL,1,0,NULL,'2026-10-26 15:50:59',NULL,NULL,NULL,NULL),(20,'shiva18@gmail.com','shiva','swamy','7845128956','$2b$12$Z8tiTglMzybm2WVJIIMgfu8HU8KocyWtFhti2DmIWPkJ77xf47RZq','buyer',NULL,NULL,'bangalore','Buyer Executive',12.9716,77.5946,1,0,NULL,'2026-10-26 16:07:26',NULL,'nri','United States','India'),(21,'pht.intern02@gmail.com','Pht','Intern15','8040480404','$2b$12$PhPnIbetnDjmCsNO..CioeieE5SdJRUJcdqrLmnh02t00ehAxUCD2','consultant',NULL,NULL,NULL,NULL,NULL,NULL,1,0,NULL,'2026-10-27 14:50:20',NULL,NULL,NULL,NULL),(22,'test_buyer_sample99@primeproperties.com','Test','Buyer','1234567890','$2b$12$81RHumso84xUypzdkM/LnuysEr3d1EgKdCLkyyA5u.ejsJzT/3osa','buyer',NULL,NULL,'Bangalore','Buyer Executive',12.9716,77.5946,1,0,NULL,'2026-10-29 16:49:43',NULL,'nri','United States','India'),(23,'ravihr08@gmail.com','ravi','hr','7845123289','$2b$12$.P0aqOytgEejJFX99asdPuvzUsoA/Tm0iU12bFi8xZlV5l0m.MaIC','owner','sale property','1-5','banhalore','Executive',NULL,NULL,1,0,NULL,'2026-11-04 16:06:24',NULL,'nri','United States','India'),(24,'jyothi@gmail.com','jyothi','yg','7845128578','$2b$12$pLaTGwzbftqanbqy3G0m2OwbY7SX1apO7iaMQjNol8NChRENruLA6','buyer',NULL,NULL,'bangalore','Buyer Executive',12.9716,77.5946,1,0,NULL,'2026-11-04 16:29:03',NULL,'nri','United States','India'),(25,'jyothihr18@gmail.com','jyothi','hr','7845120089','$2b$12$ve3bCB4b1uEgD0B16BQtM.NtaRVtVIx7OOwdtXCzxWV1hK24CRAYe','owner','property','1-5','bengalore','Executive',NULL,NULL,1,0,NULL,'2026-11-04 16:52:49',NULL,'nri','United States','India'),(26,'debug_test_user@example.com','Test','User',NULL,'$2b$12$CDL4WOuO21Dfv7BP84HMsujTeUto.6Ecr7p9lk9HpHd/uoTlG1.6.','buyer',NULL,NULL,NULL,NULL,NULL,NULL,1,0,NULL,'2026-11-05 12:15:26',NULL,NULL,NULL,NULL),(27,'live_test_user@example.com','Live','User',NULL,'$2b$12$VyD9Bp/HCVFMj7ZE6jsXV.RaGih3vXlJ3L36dWtbammTqeshTXv.y','buyer',NULL,NULL,NULL,NULL,NULL,NULL,1,0,NULL,'2026-11-05 12:20:37',NULL,NULL,NULL,NULL),(28,'jane.owner.test@example.com','Jane','Doe','9876543210','$2b$12$.7Bm/pVqBYUwxDkx0XlL7evBmjxvHPtAT6hfnCdTUCJe/hVeGDmdS','owner','Estate Corp','1-5','Bangalore','Executive',12.9716,77.5946,1,0,NULL,'2026-11-05 12:39:32',NULL,'local','India','India'),(29,'bob.consultant.test@example.com','Bob','Consultant','9876543211','$2b$12$3/niTpIq7wJsAq65W22ju.LWJxsioflYaTRhpfaiEKL29dVnnXnB2','consultant',NULL,NULL,NULL,NULL,NULL,NULL,1,0,NULL,'2026-11-05 12:39:33',NULL,NULL,NULL,NULL),(30,'verification_test_user@example.com','Verify','Tester',NULL,'$2b$12$ZCtfM4RdwFzBLtfAk2VkCOtxXM2K9mFaNN3ITpQWJoeff10F7dAeW','buyer',NULL,NULL,NULL,NULL,NULL,NULL,1,0,NULL,'2026-11-05 13:00:26',NULL,NULL,NULL,NULL),(31,'live_check_3f8c81@primeproperties.com','Health','Check',NULL,'$2b$12$FupiTXVsvmEedZyJ./V5D.0fsla.HlMp60MRroUCndKVog5wfqdjq','buyer',NULL,NULL,NULL,NULL,NULL,NULL,1,0,NULL,'2026-11-05 14:31:27',NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `visitor_info`
--

DROP TABLE IF EXISTS `visitor_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `visitor_info` (
  `id` int NOT NULL AUTO_INCREMENT,
  `full_name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT '',
  `looking_for` text COLLATE utf8mb4_unicode_ci,
  `created_at` datetime DEFAULT (now()),
  PRIMARY KEY (`id`),
  KEY `ix_visitor_info_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `visitor_info`
--

LOCK TABLES `visitor_info` WRITE;
/*!40000 ALTER TABLE `visitor_info` DISABLE KEYS */;
INSERT INTO `visitor_info` VALUES (1,'Test User','test@example.com','','','2026-11-05 11:34:53'),(2,'Live Inquiry Tester','inquiry.test@example.com','+919876543210','Bel-Air Penthouse','2026-11-05 14:31:27');
/*!40000 ALTER TABLE `visitor_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'primeproperty_v2'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-11-19 15:05:50
