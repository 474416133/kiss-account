-- Table: public.user_account

-- DROP TABLE public.user_account;

CREATE TABLE IF NOT EXISTS public.user_account
(
    password_encrypted text COLLATE pg_catalog."default",
    nickname character varying(30) COLLATE pg_catalog."default" NOT NULL,
    avatar_url character varying(300) COLLATE pg_catalog."default" NOT NULL,
    last_login_ip character varying(50) COLLATE pg_catalog."default",
    id bigint NOT NULL DEFAULT nextval('user_account_id_seq'::regclass),
    created_at timestamp without time zone NOT NULL,
    modified_at timestamp without time zone NOT NULL,
    enabled boolean NOT NULL,
    enabled_remark character varying(60) COLLATE pg_catalog."default",
    username character varying(64) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT user_account_pkey PRIMARY KEY (id),
    CONSTRAINT user_account_username_key UNIQUE (username)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.user_account
    OWNER to postgres;

COMMENT ON COLUMN public.user_account.password_encrypted
    IS '加密密码';

COMMENT ON COLUMN public.user_account.nickname
    IS '昵称';

COMMENT ON COLUMN public.user_account.avatar_url
    IS '头像url';

COMMENT ON COLUMN public.user_account.last_login_ip
    IS '最后登录时间';

COMMENT ON COLUMN public.user_account.id
    IS 'id';

COMMENT ON COLUMN public.user_account.created_at
    IS '创建时间';

COMMENT ON COLUMN public.user_account.modified_at
    IS '最近更新时间';

COMMENT ON COLUMN public.user_account.enabled
    IS '是否可用';

COMMENT ON COLUMN public.user_account.enabled_remark
    IS '备注';

COMMENT ON COLUMN public.user_account.username
    IS '用户名';


-- Table: public.user_email

-- DROP TABLE public.user_email;

CREATE TABLE IF NOT EXISTS public.user_email
(
    username character varying(64) COLLATE pg_catalog."default" NOT NULL,
    activated boolean NOT NULL,
    activate_at timestamp without time zone,
    user_id bigint NOT NULL,
    activate_ip text COLLATE pg_catalog."default",
    id bigint NOT NULL DEFAULT nextval('user_email_id_seq'::regclass),
    created_at timestamp without time zone NOT NULL,
    modified_at timestamp without time zone NOT NULL,
    CONSTRAINT user_email_pkey PRIMARY KEY (id),
    CONSTRAINT user_email_username_key UNIQUE (username),
    CONSTRAINT user_email_user_id_fkey FOREIGN KEY (user_id)
        REFERENCES public.user_account (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.user_email
    OWNER to postgres;

COMMENT ON COLUMN public.user_email.username
    IS '用户名';

COMMENT ON COLUMN public.user_email.activated
    IS '是否激活';

COMMENT ON COLUMN public.user_email.activate_at
    IS '激活时间';

COMMENT ON COLUMN public.user_email.activate_ip
    IS '激活ip';

COMMENT ON COLUMN public.user_email.id
    IS 'id';

COMMENT ON COLUMN public.user_email.created_at
    IS '创建时间';

COMMENT ON COLUMN public.user_email.modified_at
    IS '最近更新时间';


-- Table: public.user_mobile

-- DROP TABLE public.user_mobile;

CREATE TABLE IF NOT EXISTS public.user_mobile
(
    username character varying(30) COLLATE pg_catalog."default" NOT NULL,
    activated boolean NOT NULL,
    activate_at timestamp without time zone,
    user_id bigint NOT NULL,
    activate_ip text COLLATE pg_catalog."default",
    id bigint NOT NULL DEFAULT nextval('user_mobile_id_seq'::regclass),
    created_at timestamp without time zone NOT NULL,
    modified_at timestamp without time zone NOT NULL,
    CONSTRAINT user_mobile_pkey PRIMARY KEY (id),
    CONSTRAINT user_mobile_username_key UNIQUE (username),
    CONSTRAINT user_mobile_user_id_fkey FOREIGN KEY (user_id)
        REFERENCES public.user_account (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.user_mobile
    OWNER to postgres;

COMMENT ON COLUMN public.user_mobile.username
    IS '用户名';

COMMENT ON COLUMN public.user_mobile.activated
    IS '是否激活';

COMMENT ON COLUMN public.user_mobile.activate_at
    IS '激活时间';

COMMENT ON COLUMN public.user_mobile.activate_ip
    IS '激活ip';

COMMENT ON COLUMN public.user_mobile.id
    IS 'id';

COMMENT ON COLUMN public.user_mobile.created_at
    IS '创建时间';

COMMENT ON COLUMN public.user_mobile.modified_at
    IS '最近更新时间';


-- Table: public.user_password_code

-- DROP TABLE public.user_password_code;

CREATE TABLE IF NOT EXISTS public.user_password_code
(
    user_id bigint,
    username character varying(64) COLLATE pg_catalog."default" NOT NULL,
    code character varying(6) COLLATE pg_catalog."default" NOT NULL,
    expired_at bigint NOT NULL,
    client_id bigint NOT NULL,
    client_ip text COLLATE pg_catalog."default",
    id bigint NOT NULL DEFAULT nextval('user_password_code_id_seq'::regclass),
    created_at timestamp without time zone NOT NULL,
    modified_at timestamp without time zone NOT NULL,
    CONSTRAINT user_password_code_pkey PRIMARY KEY (id),
    CONSTRAINT user_password_code_user_id_fkey FOREIGN KEY (user_id)
        REFERENCES public.user_account (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.user_password_code
    OWNER to postgres;

COMMENT ON COLUMN public.user_password_code.username
    IS '用户名';

COMMENT ON COLUMN public.user_password_code.code
    IS '登录用的code';

COMMENT ON COLUMN public.user_password_code.client_id
    IS 'client_id';

COMMENT ON COLUMN public.user_password_code.client_ip
    IS '激活ip';

COMMENT ON COLUMN public.user_password_code.id
    IS 'id';

COMMENT ON COLUMN public.user_password_code.created_at
    IS '创建时间';

COMMENT ON COLUMN public.user_password_code.modified_at
    IS '最近更新时间';