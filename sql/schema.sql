-- Table: public.bankaccount

-- DROP TABLE IF EXISTS public.bankaccount;

CREATE TABLE IF NOT EXISTS public.bankaccount
(
    id integer NOT NULL DEFAULT nextval('bankaccount_id_seq'::regclass),
    user_id integer,
    bank_name character varying(100) COLLATE pg_catalog."default" NOT NULL,
    account_name character varying(50) COLLATE pg_catalog."default" NOT NULL,
    account_number text COLLATE pg_catalog."default" NOT NULL,
    balance numeric,
    currency character varying(10) COLLATE pg_catalog."default" NOT NULL,
    created_at timestamp without time zone DEFAULT now(),
    CONSTRAINT bankaccount_pkey PRIMARY KEY (id),
    CONSTRAINT bankaccount_account_number_key UNIQUE (account_number),
    CONSTRAINT bankaccount_user_id_fkey FOREIGN KEY (user_id)
        REFERENCES public.users (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT check_currency CHECK (currency::text = ANY (ARRAY['INR'::character varying, 'USD'::character varying]::text[]))
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.bankaccount
    OWNER to postgres;

-- Table: public.bankcategory

-- DROP TABLE IF EXISTS public.bankcategory;

CREATE TABLE IF NOT EXISTS public.bankcategory
(
    id integer NOT NULL DEFAULT nextval('bankcategory_id_seq'::regclass),
    name character varying(100) COLLATE pg_catalog."default" NOT NULL,
    description text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT bankcategory_pkey PRIMARY KEY (id),
    CONSTRAINT unique_name UNIQUE (name)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.bankcategory
    OWNER to postgres;


-- Table: public.banktransaction

-- DROP TABLE IF EXISTS public.banktransaction;

CREATE TABLE IF NOT EXISTS public.banktransaction
(
    id integer NOT NULL DEFAULT nextval('banktransaction_id_seq'::regclass),
    amount numeric NOT NULL,
    bank_account_id integer,
    transaction_timestamp timestamp without time zone DEFAULT now(),
    transaction_type character varying(100) COLLATE pg_catalog."default" NOT NULL,
    description text COLLATE pg_catalog."default",
    category_id integer,
    CONSTRAINT banktransaction_pkey PRIMARY KEY (id),
    CONSTRAINT banktransaction_bank_account_id_fkey FOREIGN KEY (bank_account_id)
        REFERENCES public.bankaccount (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT banktransaction_category_id_fkey FOREIGN KEY (category_id)
        REFERENCES public.bankcategory (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT transaction_type_in_credit_debit CHECK (transaction_type::text = ANY (ARRAY['credit'::character varying, 'debit'::character varying]::text[]))
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.banktransaction
    OWNER to postgres;


-- Table: public.demataccount

-- DROP TABLE IF EXISTS public.demataccount;

CREATE TABLE IF NOT EXISTS public.demataccount
(
    id integer NOT NULL DEFAULT nextval('demataccount_id_seq'::regclass),
    user_id integer,
    broker_name character varying(100) COLLATE pg_catalog."default" NOT NULL,
    account_name character varying(100) COLLATE pg_catalog."default" NOT NULL,
    broker_account_id character varying(32) COLLATE pg_catalog."default" NOT NULL,
    created_at timestamp without time zone DEFAULT now(),
    CONSTRAINT demataccount_pkey PRIMARY KEY (id),
    CONSTRAINT demataccount_broker_account_id_key UNIQUE (broker_account_id),
    CONSTRAINT demataccount_user_id_fkey FOREIGN KEY (user_id)
        REFERENCES public.users (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.demataccount
    OWNER to postgres;


-- Table: public.dematportfolio

-- DROP TABLE IF EXISTS public.dematportfolio;

CREATE TABLE IF NOT EXISTS public.dematportfolio
(
    id integer NOT NULL DEFAULT nextval('dematportfolio_id_seq'::regclass),
    demat_account_id integer,
    ticker character varying(5) COLLATE pg_catalog."default" NOT NULL,
    asset_name text COLLATE pg_catalog."default" NOT NULL,
    asset_type text COLLATE pg_catalog."default" NOT NULL,
    quantity integer NOT NULL,
    average_buy_price numeric NOT NULL,
    CONSTRAINT dematportfolio_pkey PRIMARY KEY (id),
    CONSTRAINT unique_dematportfolioaccount_ticker UNIQUE (demat_account_id, ticker),
    CONSTRAINT dematportfolio_demat_account_id_fkey FOREIGN KEY (demat_account_id)
        REFERENCES public.demataccount (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.dematportfolio
    OWNER to postgres;


-- Table: public.demattransaction

-- DROP TABLE IF EXISTS public.demattransaction;

CREATE TABLE IF NOT EXISTS public.demattransaction
(
    id integer NOT NULL DEFAULT nextval('demattransaction_id_seq'::regclass),
    portfolio_id integer,
    transaction_type text COLLATE pg_catalog."default" NOT NULL,
    quantity numeric NOT NULL,
    price_per_unit numeric NOT NULL,
    brokerage numeric NOT NULL DEFAULT 0,
    transaction_time timestamp without time zone DEFAULT now(),
    CONSTRAINT demattransaction_pkey PRIMARY KEY (id),
    CONSTRAINT demattransaction_portfolio_id_fkey FOREIGN KEY (portfolio_id)
        REFERENCES public.dematportfolio (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT buy_sell_type CHECK (transaction_type = ANY (ARRAY['buy'::text, 'sell'::text]))
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.demattransaction
    OWNER to postgres;


-- Table: public.users

-- DROP TABLE IF EXISTS public.users;

CREATE TABLE IF NOT EXISTS public.users
(
    id integer NOT NULL DEFAULT nextval('users_id_seq'::regclass),
    name character varying(100) COLLATE pg_catalog."default" NOT NULL,
    email character varying(255) COLLATE pg_catalog."default" NOT NULL,
    password_hash character varying(255) COLLATE pg_catalog."default" NOT NULL,
    created_at timestamp without time zone NOT NULL DEFAULT now(),
    CONSTRAINT users_pkey PRIMARY KEY (id),
    CONSTRAINT users_email_key UNIQUE (email)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.users
    OWNER to postgres;
-- Index: idx_users_email

-- DROP INDEX IF EXISTS public.idx_users_email;

CREATE INDEX IF NOT EXISTS idx_users_email
    ON public.users USING btree
    (email COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;