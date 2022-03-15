-- 2018-10-22
ALTER TABLE `brew_recipe` change `batch_size` `batch_size` numeric(8, 1) NOT NULL;
ALTER TABLE `brew_recipe` change `mash_tun_deadspace` `mash_tun_deadspace` numeric(7, 1) NOT NULL;
ALTER TABLE `brew_recipe` change `boiler_tun_deadspace` `boiler_tun_deadspace` numeric(7, 1) NOT NULL;
ALTER TABLE `brew_malt` change `stock_amount` `stock_amount` numeric(8, 2) NOT NULL;
ALTER TABLE `brew_hop` change `stock_amount` `stock_amount` numeric(8, 2) NOT NULL;
ALTER TABLE `brew_recipemalt` change `amount` `amount` numeric(8, 2) NOT NULL;
ALTER TABLE `brew_recipehop` change `amount` `amount` numeric(8, 2) NOT NULL;
ALTER TABLE `brew_recipehop` change `boil_time` `boil_time` numeric(8, 2) NULL;
ALTER TABLE `brew_mashstep` change `water_added` `water_added` numeric(8, 2) NULL;

-- 2015-09-25
ALTER TABLE `brew_recipe` ADD `slug_url` varchar(50);


-- 2015-09-25
ALTER TABLE "brew_malt" ADD "stock_user_id" integer REFERENCES "auth_user" ("id");
ALTER TABLE "brew_malt" ADD "stock_added" datetime;
ALTER TABLE "brew_malt" ADD "stock_amount" decimal;

ALTER TABLE "brew_hop" ADD "stock_user_id" integer REFERENCES "auth_user" ("id");
ALTER TABLE "brew_hop" ADD "stock_added" datetime;
ALTER TABLE "brew_hop" ADD "stock_amount" decimal;

ALTER TABLE "brew_yeast" ADD "stock_user_id" integer REFERENCES "auth_user" ("id");
ALTER TABLE "brew_yeast" ADD "stock_added" datetime;
ALTER TABLE "brew_yeast" ADD "stock_amount" integer;

ALTER TABLE "brew_recipemalt" ADD "malt_id" integer REFERENCES "brew_malt" ("id");
ALTER TABLE "brew_recipehop" ADD "hop_id" integer REFERENCES "brew_hop" ("id");
ALTER TABLE "brew_recipeyeast" ADD "yeast_id" integer REFERENCES "brew_yeast" ("id");

ALTER TABLE "brew_recipe" ADD "last_destock_datetime" datetime;
    

CREATE INDEX "brew_malt_20fc80c7" ON "brew_malt" ("stock_user_id");
CREATE INDEX "brew_hop_20fc80c7" ON "brew_hop" ("stock_user_id");
CREATE INDEX "brew_yeast_20fc80c7" ON "brew_yeast" ("stock_user_id");
CREATE INDEX "brew_recipemalt_7ea3b589" ON "brew_recipemalt" ("malt_id");
CREATE INDEX "brew_recipehop_5a16b9a6" ON "brew_recipehop" ("hop_id");
CREATE INDEX "brew_recipeyeast_b8100b30" ON "brew_recipeyeast" ("yeast_id");



-- 2012-12-26
ALTER TABLE `brew_recipe` ADD `modified_by_id` integer;
CREATE INDEX `brew_recipe_6162aa58` ON `brew_recipe` (`modified_by_id`);


-- 2012-11-20
ALTER TABLE `brew_recipemisc` change `amount` `amount` numeric(10, 2) NOT NULL;
ALTER TABLE `brew_recipemisc` change `time` `time` numeric(10, 2) NOT NULL;

-- 2012-11-02
ALTER TABLE `brew_recipehop` change `amount` `amount` numeric(6, 2) NOT NULL;

-- before
ALTER TABLE `brew_recipemalt` change `color` `color` numeric(7, 1) NOT NULL;


-- 2012-06-21
ALTER TABLE `brew_recipe` ADD `modified` datetime;
UPDATE `brew_recipe` SET `modified`= "2012-06-21 09:00:00";
ALTER TABLE `brew_recipe` change `modified` `modified` datetime NOT NULL;
