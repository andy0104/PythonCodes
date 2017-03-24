-- phpMyAdmin SQL Dump
-- version 4.5.2
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Mar 24, 2017 at 12:20 PM
-- Server version: 10.1.10-MariaDB
-- PHP Version: 5.6.19

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `web_crawler`
--
CREATE DATABASE IF NOT EXISTS `web_crawler` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `web_crawler`;

-- --------------------------------------------------------

--
-- Table structure for table `city`
--

DROP TABLE IF EXISTS `city`;
CREATE TABLE `city` (
  `id` int(11) NOT NULL,
  `state_id` int(11) NOT NULL,
  `county_id` int(11) NOT NULL,
  `city_name` varchar(255) CHARACTER SET latin1 NOT NULL,
  `city_url` text CHARACTER SET latin1 NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `city_links`
--

DROP TABLE IF EXISTS `city_links`;
CREATE TABLE `city_links` (
  `id` bigint(20) NOT NULL,
  `city_id` int(11) NOT NULL,
  `link_title` text CHARACTER SET latin1 NOT NULL,
  `link_url` text CHARACTER SET latin1 NOT NULL,
  `link_desc` text CHARACTER SET latin1 NOT NULL,
  `link_type` varchar(255) CHARACTER SET latin1 DEFAULT NULL,
  `final_url_reached` enum('0','1') NOT NULL DEFAULT '0',
  `date_added` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `date_updated` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `county`
--

DROP TABLE IF EXISTS `county`;
CREATE TABLE `county` (
  `id` int(11) NOT NULL,
  `state_id` int(11) NOT NULL,
  `county_name` varchar(255) CHARACTER SET latin1 NOT NULL,
  `county_url` text CHARACTER SET latin1 NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `county_links`
--

DROP TABLE IF EXISTS `county_links`;
CREATE TABLE `county_links` (
  `id` bigint(20) NOT NULL,
  `county_id` int(11) NOT NULL,
  `link_title` text CHARACTER SET latin1 NOT NULL,
  `link_url` text CHARACTER SET latin1 NOT NULL,
  `link_desc` text CHARACTER SET latin1 NOT NULL,
  `link_type` varchar(255) CHARACTER SET latin1 DEFAULT NULL,
  `final_url_reached` enum('0','1') NOT NULL DEFAULT '0',
  `date_added` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `date_updated` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `state`
--

DROP TABLE IF EXISTS `state`;
CREATE TABLE `state` (
  `id` int(11) NOT NULL,
  `state_name` varchar(255) CHARACTER SET latin1 NOT NULL,
  `state_url` text CHARACTER SET latin1 NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `state_links`
--

DROP TABLE IF EXISTS `state_links`;
CREATE TABLE `state_links` (
  `id` bigint(20) NOT NULL,
  `state_id` int(11) NOT NULL,
  `link_title` text CHARACTER SET latin1 NOT NULL,
  `link_url` text CHARACTER SET latin1 NOT NULL,
  `link_desc` text CHARACTER SET latin1 NOT NULL,
  `link_type` varchar(255) CHARACTER SET latin1 DEFAULT NULL,
  `final_url_reached` enum('0','1') NOT NULL DEFAULT '0',
  `date_added` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `date_updated` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `city`
--
ALTER TABLE `city`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `state_id` (`state_id`,`county_id`,`city_name`);

--
-- Indexes for table `city_links`
--
ALTER TABLE `city_links`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `county`
--
ALTER TABLE `county`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `county_links`
--
ALTER TABLE `county_links`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `state`
--
ALTER TABLE `state`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `state_links`
--
ALTER TABLE `state_links`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `city`
--
ALTER TABLE `city`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15303;
--
-- AUTO_INCREMENT for table `city_links`
--
ALTER TABLE `city_links`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=165;
--
-- AUTO_INCREMENT for table `county`
--
ALTER TABLE `county`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3130;
--
-- AUTO_INCREMENT for table `county_links`
--
ALTER TABLE `county_links`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8722;
--
-- AUTO_INCREMENT for table `state`
--
ALTER TABLE `state`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=56;
--
-- AUTO_INCREMENT for table `state_links`
--
ALTER TABLE `state_links`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1022;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
