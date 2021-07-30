/*
 Navicat Premium Data Transfer

 Source Server         : localhost_course_grade
 Source Server Type    : MySQL
 Source Server Version : 80025
 Source Host           : localhost:3306
 Source Schema         : course_grade

 Target Server Type    : MySQL
 Target Server Version : 80025
 File Encoding         : 65001

 Date: 30/07/2021 10:30:13
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for class
-- ----------------------------
DROP TABLE IF EXISTS `class`;
CREATE TABLE `class`  (
  `id` int(0) UNSIGNED NOT NULL AUTO_INCREMENT,
  `course_id` int(0) UNSIGNED NOT NULL,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '课程名称',
  `teacher` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '任课教师',
  `score` double(255, 2) NOT NULL COMMENT '平均分数',
  `number` int(0) UNSIGNED NOT NULL COMMENT '统计人数',
  `section_9` double(255, 2) NOT NULL COMMENT '分数区间90~100',
  `section_8` double(255, 2) NOT NULL COMMENT '分数区间80~89',
  `section_7` double(255, 2) NOT NULL COMMENT '分数区间70~79',
  `section_6` double(255, 2) NOT NULL COMMENT '分数区间60~69',
  `section_5` double(255, 2) NOT NULL COMMENT '分数区间50~59',
  `section_4` double(255, 2) NOT NULL COMMENT '分数区间40~49',
  `section_3` double(255, 2) NOT NULL COMMENT '分数区间30~39',
  `section_2` double(255, 2) NOT NULL COMMENT '分数区间20~29',
  `section_1` double(255, 2) NOT NULL COMMENT '分数区间10~19',
  `section_0` double(255, 2) NOT NULL COMMENT '分数区间0~9',
  `time` datetime(0) NOT NULL COMMENT '查询时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `course_id`(`course_id`) USING BTREE COMMENT '课程id索引',
  INDEX `course_name`(`name`) USING BTREE COMMENT '课程名索引',
  INDEX `class_score`(`score`) USING BTREE COMMENT '分数索引',
  INDEX `class_teacher`(`teacher`) USING BTREE COMMENT '教师索引',
  CONSTRAINT `course_id` FOREIGN KEY (`course_id`) REFERENCES `course` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 447 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for course
-- ----------------------------
DROP TABLE IF EXISTS `course`;
CREATE TABLE `course`  (
  `id` int(0) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '编号',
  `code` char(13) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '课程代码',
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '课程名称',
  `credit` int(0) NOT NULL COMMENT '学分',
  `category` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '课程类别',
  `subcategory` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '课程归属',
  `academy` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '开课学院',
  `time` datetime(0) NOT NULL COMMENT '查询时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `course_code`(`code`) USING BTREE COMMENT '课程代码索引',
  INDEX `course_name`(`name`) USING BTREE COMMENT '课程名称索引',
  INDEX `course_cate`(`subcategory`) USING BTREE COMMENT '课程归属索引'
) ENGINE = InnoDB AUTO_INCREMENT = 296 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
