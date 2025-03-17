/*
 Navicat MySQL Data Transfer

 Source Server         : bottle
 Source Server Type    : MySQL
 Source Server Version : 80041 (8.0.41)
 Source Host           : localhost:3306
 Source Schema         : message_bottle

 Target Server Type    : MySQL
 Target Server Version : 80041 (8.0.41)
 File Encoding         : 65001

 Date: 17/03/2025 18:40:11
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for bottles
-- ----------------------------
DROP TABLE IF EXISTS `bottles`;
CREATE TABLE `bottles`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `user_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `bottles_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of bottles
-- ----------------------------
INSERT INTO `bottles` VALUES (1, 2, '苦呀西，写代码好难QAQ，如果在给我一次机会，我一定要找几个苦力帮我干活，而不是我一只猿QAQ', '2025-03-15 15:22:04');
INSERT INTO `bottles` VALUES (2, 6, '测试测试', '2025-03-17 18:17:33');

-- ----------------------------
-- Table structure for replies
-- ----------------------------
DROP TABLE IF EXISTS `replies`;
CREATE TABLE `replies`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `bottle_id` int NOT NULL,
  `user_id` int NOT NULL,
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `bottle_id`(`bottle_id` ASC) USING BTREE,
  INDEX `user_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `replies_ibfk_1` FOREIGN KEY (`bottle_id`) REFERENCES `bottles` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `replies_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of replies
-- ----------------------------
INSERT INTO `replies` VALUES (1, 1, 3, '抱抱你哟，辛苦啦！', '2025-03-15 16:47:12');

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES (2, 'Ayanamy', '$5$rounds=535000$uwkIei9YTgP3Qpbe$mjbZ0QV0LdBXG22jRl9kON213CkUYEM.ODhQePc7qU5');
INSERT INTO `users` VALUES (3, 'tojyiku', '$5$rounds=535000$yDFcRtweqbFNJSX7$orKTv7BVxIFRgunj6mapu8HwWdssd6gjHsxIAK5pAc4');
INSERT INTO `users` VALUES (6, '一只小凌波', '$5$rounds=535000$.yvmR1t20q1uELiM$VT4KTj1uXXY.c3rlp/hw2Xy14gUKerOO0jIwHPOpJY1');

SET FOREIGN_KEY_CHECKS = 1;
