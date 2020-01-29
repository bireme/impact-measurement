-- phpMyAdmin SQL Dump
-- version 3.5.5
-- http://www.phpmyadmin.net
--
-- Servidor: mysql.teste.bireme.br
-- Tempo de Geração: 04/08/2016 às 15:35:28
-- Versão do Servidor: 5.1.57
-- Versão do PHP: 5.3.0

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Banco de Dados: `impact_measurement`
--

CREATE DATABASE IF NOT EXISTS `impact_measurement` DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci;
USE `impact_measurement`;

-- --------------------------------------------------------

--
-- Estrutura da tabela `questions`
--

CREATE TABLE IF NOT EXISTS `questions` (
  `id` bigint(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `question` varchar(300) NOT NULL DEFAULT '',
  `context` int(10) UNSIGNED NOT NULL DEFAULT '0',
  `type` int(10) UNSIGNED NOT NULL DEFAULT '0',
  `language` varchar(10) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Estrutura da tabela `questionsLocal`
--

CREATE TABLE IF NOT EXISTS `questionsLocal` (
  `id` bigint(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `question` int(10) UNSIGNED NOT NULL DEFAULT '0',
  `language` varchar(10) NOT NULL DEFAULT '',
  `label` varchar(100) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Estrutura da tabela `answers`
--

CREATE TABLE IF NOT EXISTS `answers` (
  `id` bigint(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `question` int(10) UNSIGNED NOT NULL DEFAULT '0',
  `site` int(10) UNSIGNED NOT NULL DEFAULT '0',
  `rating` int(2) NOT NULL DEFAULT '0',
  `user` varchar(100) NOT NULL DEFAULT '',
  `myvhl_user` varchar(100) NOT NULL DEFAULT '',
  `page` varchar(1000) NOT NULL DEFAULT '',
  `page_type` varchar(100) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Estrutura da tabela `context`
--

CREATE TABLE IF NOT EXISTS `contexts` (
  `id` bigint(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL DEFAULT '',
  `slug` varchar(100) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Estrutura da tabela `type`
--

CREATE TABLE IF NOT EXISTS `type` (
  `id` bigint(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL DEFAULT '',
  `slug` varchar(100) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Estrutura da tabela `websites`
--

CREATE TABLE IF NOT EXISTS `websites` (
  `id` bigint(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `code` varchar(100) NOT NULL DEFAULT '',
  `name` varchar(100) NOT NULL DEFAULT '',
  `url` varchar(1000) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
