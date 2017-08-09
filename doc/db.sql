create table product_gerdorm.dcs_basedata_enum
(
	id int not null auto_increment
		primary key,
	enum_type varchar(30) not null comment 'enum类型',
	parent_id int default '0' null comment '父层级Id，顶级为0',
	name varchar(200) not null comment '名称',
	name_ge varchar(200) not null comment '名称-德文',
	rank int(10) default '0' null comment '排序值，越小越在前',
	time_insert decimal(16,6) null comment '插入时间',
	time_update decimal(16,6) null comment '更新时间',
	status tinyint(1) default '2' null
)
comment '多语言语句'
;

create index enum_type
	on dcs_basedata_enum (enum_type)
;

create index parent_id
	on dcs_basedata_enum (parent_id)
;

create table product_gerdorm.dcs_dorm
(
	id int not null auto_increment
		primary key,
	title varchar(200) default '' not null comment '标题',
	title_ge varchar(300) default '' not null comment '标题（德）',
	title_en varchar(300) default '' not null comment '标题（英）',
	subtitle varchar(100) default '' not null comment '副标题，如：3室2厅1厨1卫 | 80m2 | 已入住1女1男',
	subtitle_ge varchar(100) default '' not null comment '副标题（德）',
	subtitle_en varchar(150) default '' not null comment '副标题（英）',
	image_list varchar(10240) default '' not null comment '图片列表，多张图用英文半角逗号(,)分开',
	rent_method int default '0' not null comment '出租类型，Biz_Dorm_Enum_RentMethod',
	room_amount smallint(4) default '0' not null comment '房间数',
	usable_area smallint(4) default '0' not null comment '可用面积（平方米）',
	floor_current smallint(4) default '0' not null comment '当前楼层',
	floor_all smallint(4) default '0' not null comment '所有楼层',
	rent_fee_cold decimal(12,2) default '0.00' not null comment '冷月租金',
	rent_fee_addon decimal(12,2) default '0.00' not null comment '附加费用',
	rent_fee_other decimal(12,2) default '0.00' not null comment '其他费用',
	rent_fee_deposit decimal(12,2) default '0.00' not null comment '押金',
	rent_fee_undertaking decimal(12,2) default '0.00' not null comment '承接费用',
	attribute_furniture tinyint(1) default '0' not null comment '房屋配置：带家具',
	attribute_tv tinyint(1) default '0' not null comment '房屋配置：电视机',
	attribute_heating tinyint(1) default '0' not null comment '房屋配置：暖气',
	attribute_refrigerator tinyint(1) default '0' not null comment '房屋配置：冰箱',
	attribute_washer tinyint(1) default '0' not null comment '房屋配置：洗衣机',
	attribute_wired tinyint(1) default '0' not null comment '房屋配置：有线网络',
	attribute_wifi tinyint(1) default '0' not null comment '房屋配置：无线网络',
	attribute_bathroom tinyint(1) default '0' not null comment '房屋配置：沐浴室',
	attribute_bathtub tinyint(1) default '0' not null comment '房屋配置：浴缸',
	feature_elevator tinyint(1) default '0' not null comment '周边配套：电梯',
	feature_entrance_guard tinyint(1) default '0' not null comment '周边配套：门禁',
	feature_garden tinyint(1) default '0' not null comment '周边配套：花园',
	feature_basement tinyint(1) default '0' not null comment '周边配套：地下室',
	feature_parking_space tinyint(1) default '0' not null comment '周边配套：停车位',
	feature_bike_parking tinyint(1) default '0' not null comment '周边配套：自行车位',
	feature_subway tinyint(1) default '0' not null comment '周边配套：地铁',
	feature_bus tinyint(1) default '0' not null comment '周边配套：巴士',
	feature_hospital tinyint(1) default '0' not null comment '周边配套：医院',
	feature_supermarket tinyint(1) default '0' not null comment '周边配套：超市',
	attention_allow_pet tinyint(1) default '0' not null comment '注意事项：允许养宠物',
	attention_allow_cooking tinyint(1) default '0' not null comment '注意事项：允许做饭',
	description longtext null comment '房屋描述',
	description_ge longtext null comment '房屋描述（德）',
	description_en longtext null comment '房屋描述（英）',
	time_rent_begin int(10) default '0' not null comment '可租起止时间：起始时间',
	time_rent_end int(10) default '0' not null comment '可租起止时间：截止时间，为0时表示可长租',
	rent_shortest_days int default '0' not null comment '可租起止时间：最短租期（天）',
	view_count int default '0' not null comment '浏览人数',
	location_name varchar(100) default '' not null comment '位置信息内容',
	location_longitude decimal(11,8) default '0.00000000' not null comment '位置：经度',
	location_latitude decimal(11,8) default '0.00000000' not null comment '位置：纬度',
	state varchar(100) default '' not null comment '状态列表',
	rank int default '0' not null comment '排序，越大越靠前',
	time_insert decimal(16,6) default '0.000000' not null comment '插入时间',
	time_update decimal(16,6) default '0.000000' not null comment '更新时间',
	status tinyint(1) default '1' null,
	rent_fee_hot decimal(12,2) default '0.00' not null comment '暖月租金',
	publisher_type varchar(50) default '' not null comment '发布者类型：中介／个人',
	publisher_name varchar(100) default '' not null comment '发布者称呼',
	publisher_contact varchar(50) default '' not null comment '发布者联系方式',
	source_view_count int default '0' not null comment '数据源浏览数',
	source_link varchar(1024) default '' not null comment '原始链接',
	source_publish_time int default '0' not null comment '原始发布时间（时间戳）',
	attribute_bed tinyint(1) default '0' not null comment '房屋配置：床',
	attribute_balcony tinyint(1) default '0' not null comment '房屋配置：阳台',
	attribute_terrace tinyint(1) default '0' not null comment '房屋配置：露台',
	attribute_disability tinyint(1) default '0' not null comment '房屋配置：残疾人',
	feature_loft tinyint(1) default '0' not null comment '周边配套：阁楼',
	attention_can_be_settled tinyint(1) default '0' not null comment '注意事项：可落户',
	attention_welfare_in tinyint(1) default '0' not null comment '注意事项：需福利准入证',
	attention_joint_rent tinyint(1) default '0' not null comment '注意事项：允许合租',
	layout_kitchen tinyint(1) default '0' not null comment '户型：厨房',
	layout_lavatory tinyint(1) default '0' not null comment '户型：厕所',
	other_new_building tinyint(1) default '0' not null comment '房屋年代-新建筑',
	attention_checkin_any_time tinyint(1) default '0' not null comment '注意事项：随时入住',
	zip_code varchar(50) default '' not null comment '邮编',
	city varchar(200) default '' not null comment '城市'
)
comment '房屋'
;

create index rent_method
	on dcs_dorm (rent_method)
;

create index room_amount
	on dcs_dorm (room_amount)
;

create index status
	on dcs_dorm (status)
;

create table product_gerdorm.names
(
	id tinyint(3) unsigned not null auto_increment
		primary key,
	name varchar(30) default '' not null,
	info text null,
	age tinyint(3) unsigned default '30' null
)
;

