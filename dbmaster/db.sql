SET NAMES utf8;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
--  Table structure for `accounts`
-- ----------------------------
DROP TABLE IF EXISTS `accounts`;
CREATE TABLE `accounts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `passwd` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `login_name` varchar(64) CHARACTER SET utf8 DEFAULT NULL,
  `mobile` varchar(16) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `city` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '所在城市',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=COMPACT;

-- ----------------------------
--  Table structure for `query_log`
-- ----------------------------
DROP TABLE IF EXISTS `query_log`;
CREATE TABLE `query_log` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `account_id` int(11) DEFAULT NULL,
  `account_name` varchar(64) CHARACTER SET utf8mb4 DEFAULT NULL,
  `op_ip` varchar(20) CHARACTER SET utf8mb4 DEFAULT NULL,
  `op_time` datetime DEFAULT NULL,
  `content` text CHARACTER SET utf8mb4,
  `cost_time` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '执行耗时',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=COMPACT;

-- ----------------------------
--  Table structure for `syslog`
-- ----------------------------
DROP TABLE IF EXISTS `syslog`;
CREATE TABLE `syslog` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `account_id` int(11) DEFAULT NULL,
  `account_name` varchar(64) CHARACTER SET utf8mb4 DEFAULT NULL,
  `op_ip` varchar(20) CHARACTER SET utf8mb4 DEFAULT NULL,
  `op_time` datetime DEFAULT NULL,
  `content` text CHARACTER SET utf8mb4,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=COMPACT;

-- ----------------------------
--  Table structure for `update_application`
-- ----------------------------
DROP TABLE IF EXISTS `update_application`;
CREATE TABLE `update_application` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `account_id` int(11) DEFAULT NULL,
  `account_name` varchar(64) CHARACTER SET utf8mb4 DEFAULT NULL,
  `reason` varchar(1024) CHARACTER SET utf8mb4 DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `sql_content` text CHARACTER SET utf8mb4,
  `status` int(32) DEFAULT NULL COMMENT '状态',
  `opt_account_id` int(11) DEFAULT NULL,
  `opt_account_name` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=COMPACT;


INSERT INTO `accounts` VALUES ('1', 'dba', 'admin', '2017-03-31 13:19:22', 'admin', null, null);