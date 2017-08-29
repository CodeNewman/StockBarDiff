/*
Navicat SQLite Data Transfer

Source Server         : stocks-bar
Source Server Version : 31300
Source Host           : :0

Target Server Type    : SQLite
Target Server Version : 31300
File Encoding         : 65001

Date: 2017-08-24 14:44:04
*/

PRAGMA foreign_keys = OFF;

-- ----------------------------
-- Table structure for u_stock_bar_data
-- ----------------------------
DROP TABLE IF EXISTS "main"."u_stock_bar_data";
CREATE TABLE "u_stock_bar_data" (
"stock_code"  TEXT NOT NULL,
"date"  TEXT,
"beta_open"  TEXT,
"beta_high"  TEXT,
"beta_low"  TEXT,
"beta_close"  TEXT,
"beta_vol"  TEXT,
"beta_adj_open"  TEXT,
"beta_adj_high"  TEXT,
"beta_adj_low"  TEXT,
"beta_adj_close"  TEXT,
"beta_adj_vol"  TEXT,
"local_open"  TEXT,
"local_high"  TEXT,
"local_low"  TEXT,
"local_close"  TEXT,
"local_vol"  TEXT,
"local_adj_open"  TEXT,
"local_adj_high"  TEXT,
"local_adj_low"  TEXT,
"local_adj_close"  TEXT,
"local_adj_vol"  TEXT,
"diff_open"  TEXT,
"diff_high"  TEXT,
"diff_low"  TEXT,
"diff_close"  TEXT,
"diff_vol"  TEXT,
"diff_adj_open"  TEXT,
"diff_adj_high"  TEXT,
"diff_adj_low"  TEXT,
"diff_adj_close"  TEXT,
"diff_adj_vol"  TEXT
);

-- ----------------------------
-- Indexes structure for table u_stock_bar_data
-- ----------------------------
CREATE INDEX "main".""
ON "u_stock_bar_data" ("stock_code" ASC);
PRAGMA foreign_keys = ON;
