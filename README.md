# bioSignalPro
Bioelectrical signal processing

##  技术选型
### 前端框架：

**React.js + D3.js / Plotly**：
  
* React.js 用于构建动态的用户界面，响应式的可视化组件。
* D3.js 或 Plotly 可以用来绘制动态且交互丰富的生物电信号图表。D3.js 是一个强大的 JavaScript 库，用于数据驱动的文档操作，可以制作高度自定义的图表。Plotly 是一个基于 D3.js 的高阶库，适合快速构建交互式图表，支持数据放大、缩小等功能。

### 后端框架：

**Django + Django Channels：**

* Django 是一个成熟的 Web 框架，可以用来处理请求和响应，以及数据库操作。
* Django Channels 支持 WebSockets 和异步请求，可以有效处理实时数据流。适用于实时显示生物电信号数据流（例如通过 WebSockets 向前端发送更新的信号数据）。

### 数据存储：

**数据库：MySQL / PostgreSQL + Time Series Database (TSDB)：**

* MySQL 或 PostgreSQL 用于存储基本的用户信息和非时序数据（例如用户 ID、设备信息等）。
* 对于生物信号数据，考虑使用 时序数据库（如 InfluxDB 或 TimescaleDB），因为它们能高效存储和查询时序数据，如每秒采集的数据。
### 数据流：

**数据分块存储和流式处理：**
* 为了避免一次性加载大量数据到内存，可以将数据分为多个小块（例如，按时间段或信号通道划分），每次只加载必要的部分进行处理。
* **数据分页**：在前端显示时，采用分页加载的方式（例如，按时间段加载）进行数据渲染，减少内存消耗。

**缓存和数据预处理：**

* **Redis** 用于缓存常用的生物信号数据或计算结果，减少频繁访问数据库的压力。
* **Celery** 可以作为后台任务处理系统，用于对生物信号数据进行预处理和聚合，定时将信号数据分块存储，并优化查询。
数据压缩：

对录制的生物信号数据进行压缩存储，减少磁盘空间占用。常用的压缩方法包括 HDF5 格式、Parquet 格式等，特别适合时序数据。

## 架构设计
### 前端（React.js）：

* 显示一个时间线上的生物信号，支持放大缩小、拖拽操作。

* 数据按时间段加载：用户请求查看某个时段的信号时，前端通过 API 请求后台加载对应时间段的数据。

* 支持多通道显示和交互操作，允许用户选择查看不同的信号通道。
### 后端（Django + Django Channels）：

* Django REST API：提供数据查询接口，允许前端请求按时间段、按通道、按用户等条件获取生物信号数据。
* Django Channels：通过 WebSockets 向前端实时推送数据更新，适合处理实时的生物信号数据流。
* Celery：用于处理后台任务，比如数据的批量加载、信号处理等。
### 数据库设计：

* MySQL/PostgreSQL：存储用户信息、设备信息等元数据。
* InfluxDB / TimescaleDB：存储生物信号数据，按时间顺序存储每个通道的数据点。
### 数据存储和流式处理：

* 数据分块存储：将生物信号数据分块存储（按时间段或通道划分），每次请求只加载需要的数据块。
* 分页加载：通过前端分页加载数据，每次只加载一个时间段的数据，避免加载过多数据导致内存溢出。

##  数据库表设计
### 用户信息表
存储用户的基本信息和与设备相关的信息。
```sql
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
### 设备信息表（devices）
存储设备相关信息，每个用户可能有多个设备。
```sql
CREATE TABLE devices (
    device_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    device_name VARCHAR(255),
    device_type VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
```
### 生物信号数据表（bio_signals）
存储每个通道的生物信号数据，数据按时间顺序存储。
```sql
CREATE TABLE bio_signals (
    signal_id SERIAL PRIMARY KEY,
    device_id INT,
    timestamp TIMESTAMP NOT NULL,  -- 时间戳
    channel INT NOT NULL,          -- 信号通道，例如 EEG, ECG
    signal_value FLOAT NOT NULL,   -- 信号值，存储浮动的生物信号
    FOREIGN KEY (device_id) REFERENCES devices(device_id)
);
```
### 信号数据存储表（signal_chunks）
考虑到生物信号数据量大，可以将数据按时间段或通道分块存储，优化查询和加载。
```sql
CREATE TABLE signal_chunks (
    chunk_id SERIAL PRIMARY KEY,
    device_id INT,
    channel INT,                 -- 信号通道
    start_time TIMESTAMP NOT NULL,  -- 数据开始时间
    end_time TIMESTAMP NOT NULL,    -- 数据结束时间
    chunk_data BYTEA,             -- 存储压缩后的生物信号数据块（如 HDF5 或 Parquet 格式）
    FOREIGN KEY (device_id) REFERENCES devices(device_id)
);
```

### 用户活动记录表（user_activity）
记录用户的交互和查询活动，例如查询某一时间段的数据，支持日志和统计分析。
```sql
CREATE TABLE user_activity (
    activity_id SERIAL PRIMARY KEY,
    user_id INT,
    action_type VARCHAR(255),      -- 操作类型：查询、浏览、下载等
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB,               -- 存储附加信息，如查询条件、参数等
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
```