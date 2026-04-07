-- Таблица пользователей
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    premium BOOLEAN DEFAULT 0,
    premium_until INTEGER,
    twitch_login TEXT,
    twitch_user_id TEXT,
    twitch_access_token TEXT,
    twitch_refresh_token TEXT,
    vk_user_id TEXT,
    vk_access_token TEXT,
    main_chat_id INTEGER,
    extra_chats TEXT DEFAULT '[]',
    message_template TEXT DEFAULT '✨ {channel} начал стрим на {platform}!\n🎮 {title}\n👉 {url}',
    banner_file_id TEXT,
    monitor_active BOOLEAN DEFAULT 1,
    notif_start BOOLEAN DEFAULT 1,
    notif_end BOOLEAN DEFAULT 0,
    notif_title BOOLEAN DEFAULT 0,
    notif_category BOOLEAN DEFAULT 0,
    cooldown_start INTEGER DEFAULT 0,
    cooldown_end INTEGER DEFAULT 0,
    cooldown_title INTEGER DEFAULT 60,
    cooldown_category INTEGER DEFAULT 60,
    last_notified_start INTEGER,
    last_notified_end INTEGER,
    last_notified_title INTEGER,
    last_notified_category INTEGER,
    stats_total INTEGER DEFAULT 0,
    stats_twitch INTEGER DEFAULT 0,
    stats_vk INTEGER DEFAULT 0,
    last_stream_platform TEXT,
    last_stream_title TEXT,
    last_stream_timestamp INTEGER,
    ref_code TEXT UNIQUE,
    ref_invited TEXT DEFAULT '[]',
    ref_by INTEGER,
    created_at INTEGER
);

-- Таблица премиум кодов
CREATE TABLE IF NOT EXISTS premium_codes (
    code TEXT PRIMARY KEY,
    days INTEGER,
    used BOOLEAN DEFAULT 0,
    used_by INTEGER,
    used_at INTEGER,
    created_at INTEGER
);

-- Таблица логов уведомлений
CREATE TABLE IF NOT EXISTS notification_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    chat_id INTEGER,
    platform TEXT,
    event_type TEXT,
    sent_at INTEGER
);

-- Индексы для оптимизации
CREATE INDEX IF NOT EXISTS idx_users_ref_code ON users(ref_code);
CREATE INDEX IF NOT EXISTS idx_users_main_chat ON users(main_chat_id);
CREATE INDEX IF NOT EXISTS idx_notification_logs_user ON notification_logs(user_id);

-- Таблица чатов бота (для отслеживания)
CREATE TABLE IF NOT EXISTS bot_chats (
    chat_id INTEGER PRIMARY KEY,
    chat_type TEXT,
    title TEXT,
    added_at INTEGER
);

-- Таблица администраторов чатов
CREATE TABLE IF NOT EXISTS chat_admins (
    chat_id INTEGER,
    user_id INTEGER,
    is_admin BOOLEAN DEFAULT 1,
    PRIMARY KEY (chat_id, user_id)
);