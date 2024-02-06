--
-- PostgreSQL database dump
--

-- Dumped from database version 13.10
-- Dumped by pg_dump version 15.3

-- Started on 2023-11-27 19:09:49

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 32 (class 2615 OID 10936308)
-- Name: scheduling_dev; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA scheduling_dev;


ALTER SCHEMA scheduling_dev OWNER TO postgres;

--
-- TOC entry 1175 (class 1255 OID 10993489)
-- Name: booking_logs(); Type: FUNCTION; Schema: scheduling_dev; Owner: postgres
--

CREATE FUNCTION scheduling_dev.booking_logs() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
	IF TG_OP = 'INSERT' THEN
INSERT INTO "scheduling_dev"."booking_logs" ("id", "business_id", "customer_id", "type", "start_time", "initiator", "status", "recurring", "edited", "created_at", "duration", "operation")
VALUES(NEW.id,NEW.business_id,NEW.customer_id,NEW.type,NEW.start_time,NEW.initiator,NEW.status,NEW.recurring,NEW.edited,NEW.created_at,NEW.duration,'INSERT');
	ELSIF TG_OP = 'UPDATE' THEN
INSERT INTO "scheduling_dev"."booking_logs" ("id", "business_id", "customer_id", "type", "start_time", "initiator", "status", "recurring", "edited", "created_at", "duration", "operation")
VALUES(OLD.id,NEW.business_id,OLD.customer_id,OLD.type,OLD.start_time,OLD.initiator,OLD.status,OLD.recurring,OLD.edited,OLD.created_at,OLD.duration,'UPDATE');
	ELSIF TG_OP = 'DELETE' THEN
INSERT INTO "scheduling_dev"."booking_logs" ("id", "business_id", "customer_id", "type", "start_time", "initiator", "status", "recurring", "edited", "created_at", "duration", "operation")
VALUES(OLD.id,OLD.business_id,OLD.customer_id,OLD.type,OLD.start_time,OLD.initiator,OLD.status,OLD.recurring,OLD.edited,OLD.created_at,OLD.duration,'DELETE');
	END IF;
	RETURN NEW;
END;
$$;


ALTER FUNCTION scheduling_dev.booking_logs() OWNER TO postgres;

--
-- TOC entry 1177 (class 1255 OID 11003347)
-- Name: business_logs(); Type: FUNCTION; Schema: scheduling_dev; Owner: postgres
--

CREATE FUNCTION scheduling_dev.business_logs() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
	IF TG_OP = 'INSERT' THEN
		INSERT INTO "scheduling_dev"."business_logs" ("id", "biz_name", "owner_first_name", "owner_last_name", "address", "city", "state", "latitude", "longitude", "phone", "email", "auto_approve", "cancellation_policy", "created_at", "timezone", "enabled", "get_started", "operation")
			VALUES(NEW.id, NEW.biz_name, NEW. "owner_first_name", NEW. "owner_last_name", NEW. "address", NEW. "city", NEW. "state", NEW. "latitude", NEW. "longitude", NEW. "phone", NEW. "email", NEW. "auto_approve", NEW. "cancellation_policy", NEW. "created_at", NEW. "timezone", NEW. "enabled", NEW. "get_started", 'INSERT');
	ELSIF TG_OP = 'UPDATE' THEN
		INSERT INTO "scheduling_dev"."business_logs" ("id", "biz_name", "owner_first_name", "owner_last_name", "address", "city", "state", "latitude", "longitude", "phone", "email", "auto_approve", "cancellation_policy", "created_at", "timezone", "enabled", "get_started", "operation")
			VALUES(OLD.id, OLD.biz_name, OLD. "owner_first_name", OLD. "owner_last_name", OLD. "address", OLD. "city", OLD. "state", OLD. "latitude", OLD. "longitude", OLD. "phone", OLD. "email", OLD. "auto_approve", OLD. "cancellation_policy", OLD. "created_at", OLD. "timezone", OLD. "enabled", OLD. "get_started", 'UPDATE');
	ELSIF TG_OP = 'DELETE' THEN
		INSERT INTO "scheduling_dev"."business_logs" ("id", "biz_name", "owner_first_name", "owner_last_name", "address", "city", "state", "latitude", "longitude", "phone", "email", "auto_approve", "cancellation_policy", "created_at", "timezone", "enabled", "get_started", "operation")
			VALUES(OLD.id, OLD.biz_name, OLD. "owner_first_name", OLD. "owner_last_name", OLD. "address", OLD. "city", OLD. "state", OLD. "latitude", OLD. "longitude", OLD. "phone", OLD. "email", OLD. "auto_approve", OLD. "cancellation_policy", OLD. "created_at", OLD. "timezone", OLD. "enabled", OLD. "get_started", 'DELETE');
	END IF;
	RETURN NEW;
END;
$$;


ALTER FUNCTION scheduling_dev.business_logs() OWNER TO postgres;

--
-- TOC entry 1178 (class 1255 OID 11107465)
-- Name: categories_logs(); Type: FUNCTION; Schema: scheduling_dev; Owner: postgres
--

CREATE FUNCTION scheduling_dev.categories_logs() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
	IF TG_OP = 'INSERT' THEN
		INSERT INTO "scheduling_dev"."category_logs" ("id", "name", "photo", "description", "business_id", "created_at", "deleted","operation")
			VALUES(NEW.id, NEW.name, NEW.photo, NEW.description, NEW.business_id, NEW.created_at, NEW.deleted, 'INSERT');
	ELSIF TG_OP = 'UPDATE' THEN
		INSERT INTO "scheduling_dev"."category_logs" ("id", "name", "photo", "description", "business_id", "created_at", "deleted","operation")
			VALUES(OLD.id, OLD.name, OLD.photo, OLD.description, OLD.business_id, OLD.created_at, OLD.deleted, 'UPDATE');
	ELSIF TG_OP = 'DELETE' THEN
		INSERT INTO "scheduling_dev"."category_logs" ("id", "name", "photo", "description", "business_id", "created_at", "deleted","operation")
			VALUES(OLD.id, OLD.name, OLD.photo, OLD.description, OLD.business_id, OLD.created_at, OLD.deleted, 'DELETE');
	END IF;
	RETURN NEW;
END;
$$;


ALTER FUNCTION scheduling_dev.categories_logs() OWNER TO postgres;

--
-- TOC entry 1174 (class 1255 OID 10993458)
-- Name: line_item_logs(); Type: FUNCTION; Schema: scheduling_dev; Owner: postgres
--

CREATE FUNCTION scheduling_dev.line_item_logs() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
	IF TG_OP = 'INSERT' THEN
		INSERT INTO "scheduling_dev"."line_item_logs" ("id", "booking_id", "pro_id", "service_id", "service_variation_id", "created_at", "operation")
			VALUES(NEW.id, NEW.booking_id, NEW.pro_id, NEW.service_id, NEW.service_variation_id, NEW.created_at, 'INSERT');
	ELSIF TG_OP = 'UPDATE' THEN
		INSERT INTO "scheduling_dev"."line_item_logs" ("id", "booking_id", "pro_id", "service_id", "service_variation_id", "created_at", "operation")
			VALUES(OLD.id, OLD.booking_id, OLD.pro_id, OLD.service_id, OLD.service_variation_id, OLD.created_at, 'UPDATE');
	ELSIF TG_OP = 'DELETE' THEN
		INSERT INTO "scheduling_dev"."line_item_logs" ("id", "booking_id", "pro_id", "service_id", "service_variation_id", "created_at", "operation")
			VALUES(OLD.id, OLD.booking_id, OLD.pro_id, OLD.service_id, OLD.service_variation_id, OLD.created_at, 'DELETE');
	END IF;
	RETURN NEW;
END;
$$;


ALTER FUNCTION scheduling_dev.line_item_logs() OWNER TO postgres;

--
-- TOC entry 1179 (class 1255 OID 11107701)
-- Name: services_logs(); Type: FUNCTION; Schema: scheduling_dev; Owner: postgres
--

CREATE FUNCTION scheduling_dev.services_logs() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
	IF TG_OP = 'INSERT' THEN
		INSERT INTO "scheduling_dev"."service_logs" ("id", "business_id", "name", "category", "description", "photo", "created_at","category_id","deleted",operation)
			VALUES(NEW.id, NEW.business_id, NEW.name, NEW.category, NEW.description, NEW.photo, NEW.created_at,NEW.category_id,NEW.deleted, 'INSERT');
	ELSIF TG_OP = 'UPDATE' THEN
		INSERT INTO "scheduling_dev"."service_logs" ("id", "business_id", "name", "category", "description", "photo", "created_at","category_id","deleted",operation)
			VALUES(NEW.id, NEW.business_id, NEW.name, NEW.category, NEW.description, NEW.photo, NEW.created_at,NEW.category_id,NEW.deleted, 'UPDATE');
	ELSIF TG_OP = 'DELETE' THEN
		INSERT INTO "scheduling_dev"."service_logs" ("id", "business_id", "name", "category", "description", "photo", "created_at","category_id","deleted",operation)
			VALUES(OLD.id, OLD.business_id, OLD.name, OLD.category, OLD.description, OLD.photo, OLD.created_at,OLD.category_id,OLD.deleted, 'DELETE');
	END IF;
	RETURN NEW;
END;
$$;


ALTER FUNCTION scheduling_dev.services_logs() OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 871 (class 1259 OID 10993472)
-- Name: booking_logs; Type: TABLE; Schema: scheduling_dev; Owner: postgres
--

CREATE TABLE scheduling_dev.booking_logs (
    id uuid,
    business_id uuid,
    customer_id uuid,
    type character varying,
    start_time timestamp without time zone,
    initiator character varying,
    status character varying,
    recurring character varying,
    rescheduled_id uuid,
    edited boolean,
    call_count integer,
    message_count integer,
    created_at timestamp without time zone,
    duration integer,
    primary_id integer NOT NULL,
    timestamp_ timestamp without time zone DEFAULT now(),
    operation character varying DEFAULT ''::character varying
);


ALTER TABLE scheduling_dev.booking_logs OWNER TO postgres;

--
-- TOC entry 872 (class 1259 OID 10993481)
-- Name: booking_primary_id_seq; Type: SEQUENCE; Schema: scheduling_dev; Owner: postgres
--

ALTER TABLE scheduling_dev.booking_logs ALTER COLUMN primary_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME scheduling_dev.booking_primary_id_seq
    START WITH 0
    INCREMENT BY 1
    MINVALUE 0
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 665 (class 1259 OID 10937463)
-- Name: bookings; Type: TABLE; Schema: scheduling_dev; Owner: postgres
--

CREATE TABLE scheduling_dev.bookings (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    business_id uuid,
    customer_id uuid,
    type character varying,
    start_time timestamp without time zone,
    initiator character varying,
    status character varying,
    recurring character varying,
    rescheduled_id uuid,
    edited boolean,
    call_count integer,
    message_count integer,
    created_at timestamp without time zone DEFAULT now(),
    duration integer DEFAULT 0
);


ALTER TABLE scheduling_dev.bookings OWNER TO postgres;

--
-- TOC entry 921 (class 1259 OID 11037583)
-- Name: bookings_dev; Type: TABLE; Schema: scheduling_dev; Owner: postgres
--

CREATE TABLE scheduling_dev.bookings_dev (
    id uuid DEFAULT public.uuid_generate_v4(),
    business_id uuid,
    customer_id uuid,
    type character varying,
    start_time timestamp without time zone,
    initiator character varying,
    status character varying,
    recurring character varying,
    rescheduled_id uuid,
    edited boolean,
    call_count integer,
    message_count integer,
    created_at timestamp without time zone,
    duration integer
);


ALTER TABLE scheduling_dev.bookings_dev OWNER TO postgres;

--
-- TOC entry 877 (class 1259 OID 11003032)
-- Name: business_logs; Type: TABLE; Schema: scheduling_dev; Owner: postgres
--

CREATE TABLE scheduling_dev.business_logs (
    id uuid NOT NULL,
    biz_name character varying NOT NULL,
    owner_first_name character varying,
    owner_last_name character varying,
    address character varying,
    city character varying,
    state character varying,
    latitude double precision,
    longitude double precision,
    phone character varying,
    email character varying,
    auto_approve boolean,
    cancellation_policy character varying,
    created_at timestamp without time zone,
    zip_code character varying,
    timezone character varying,
    enabled boolean,
    get_started boolean,
    primary_id integer NOT NULL,
    operation character varying,
    timestamp_ timestamp without time zone DEFAULT now()
);


ALTER TABLE scheduling_dev.business_logs OWNER TO postgres;

--
-- TOC entry 878 (class 1259 OID 11003299)
-- Name: business_logs_primary_id_seq; Type: SEQUENCE; Schema: scheduling_dev; Owner: postgres
--

ALTER TABLE scheduling_dev.business_logs ALTER COLUMN primary_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME scheduling_dev.business_logs_primary_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 659 (class 1259 OID 10936365)
-- Name: businesses; Type: TABLE; Schema: scheduling_dev; Owner: postgres
--

CREATE TABLE scheduling_dev.businesses (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    biz_name character varying NOT NULL,
    owner_first_name character varying,
    owner_last_name character varying,
    address character varying,
    city character varying,
    state character varying,
    latitude double precision,
    longitude double precision,
    phone character varying,
    email character varying,
    auto_approve boolean,
    cancellation_policy character varying,
    created_at timestamp without time zone DEFAULT now(),
    zip_code character varying,
    timezone character varying,
    enabled boolean DEFAULT false,
    get_started boolean DEFAULT false
);


ALTER TABLE scheduling_dev.businesses OWNER TO postgres;

--
-- TOC entry 672 (class 1259 OID 10942269)
-- Name: categories; Type: TABLE; Schema: scheduling_dev; Owner: postgres
--

CREATE TABLE scheduling_dev.categories (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    name character varying,
    photo character varying,
    description character varying,
    business_id uuid,
    created_at timestamp without time zone DEFAULT now(),
    deleted boolean DEFAULT false
);


ALTER TABLE scheduling_dev.categories OWNER TO postgres;

--
-- TOC entry 1062 (class 1259 OID 11107472)
-- Name: category_logs; Type: TABLE; Schema: scheduling_dev; Owner: postgres
--

CREATE TABLE scheduling_dev.category_logs (
    id uuid,
    name character varying,
    photo character varying,
    description character varying,
    business_id uuid,
    created_at timestamp without time zone,
    deleted boolean DEFAULT false,
    primary_id integer NOT NULL,
    operation character varying,
    timestamp_ timestamp without time zone DEFAULT now()
);


ALTER TABLE scheduling_dev.category_logs OWNER TO postgres;

--
-- TOC entry 1061 (class 1259 OID 11107470)
-- Name: category_logs_primary_id_seq; Type: SEQUENCE; Schema: scheduling_dev; Owner: postgres
--

CREATE SEQUENCE scheduling_dev.category_logs_primary_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE scheduling_dev.category_logs_primary_id_seq OWNER TO postgres;

--
-- TOC entry 7518 (class 0 OID 0)
-- Dependencies: 1061
-- Name: category_logs_primary_id_seq; Type: SEQUENCE OWNED BY; Schema: scheduling_dev; Owner: postgres
--

ALTER SEQUENCE scheduling_dev.category_logs_primary_id_seq OWNED BY scheduling_dev.category_logs.primary_id;


--
-- TOC entry 690 (class 1259 OID 10975529)
-- Name: comms_content; Type: TABLE; Schema: scheduling_dev; Owner: postgres
--

CREATE TABLE scheduling_dev.comms_content (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    business_id uuid,
    recipient_type character varying,
    comm_type character varying,
    text character varying,
    service character varying DEFAULT 'SMS'::character varying,
    reminder_minutes integer
);


ALTER TABLE scheduling_dev.comms_content OWNER TO postgres;

--
-- TOC entry 664 (class 1259 OID 10937454)
-- Name: customers; Type: TABLE; Schema: scheduling_dev; Owner: postgres
--

CREATE TABLE scheduling_dev.customers (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    business_id uuid,
    first_name character varying,
    phone character varying,
    email character varying,
    date_of_birth date,
    type character varying,
    created_at timestamp without time zone DEFAULT now(),
    last_name character varying,
    lead_type character varying
);


ALTER TABLE scheduling_dev.customers OWNER TO postgres;

--
-- TOC entry 869 (class 1259 OID 10993443)
-- Name: line_item_logs; Type: TABLE; Schema: scheduling_dev; Owner: postgres
--

CREATE TABLE scheduling_dev.line_item_logs (
    id uuid,
    booking_id uuid,
    pro_id uuid,
    service_id uuid,
    service_variation_id uuid,
    preferred_pro boolean,
    created_at timestamp without time zone,
    primary_id integer NOT NULL,
    timestamp_ timestamp without time zone DEFAULT now(),
    operation character varying
);


ALTER TABLE scheduling_dev.line_item_logs OWNER TO postgres;

--
-- TOC entry 870 (class 1259 OID 10993454)
-- Name: line_item_logs_primary_id_seq; Type: SEQUENCE; Schema: scheduling_dev; Owner: postgres
--

ALTER TABLE scheduling_dev.line_item_logs ALTER COLUMN primary_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME scheduling_dev.line_item_logs_primary_id_seq
    START WITH 0
    INCREMENT BY 1
    MINVALUE 0
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 666 (class 1259 OID 10937472)
-- Name: line_items; Type: TABLE; Schema: scheduling_dev; Owner: postgres
--

CREATE TABLE scheduling_dev.line_items (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    booking_id uuid,
    pro_id uuid,
    service_id uuid,
    service_variation_id uuid,
    preferred_pro boolean,
    created_at timestamp without time zone DEFAULT now()
);


ALTER TABLE scheduling_dev.line_items OWNER TO postgres;

--
-- TOC entry 922 (class 1259 OID 11037873)
-- Name: line_items_dev; Type: TABLE; Schema: scheduling_dev; Owner: postgres
--

CREATE TABLE scheduling_dev.line_items_dev (
    id uuid DEFAULT public.uuid_generate_v4(),
    booking_id uuid,
    pro_id uuid,
    service_id uuid,
    service_variation_id uuid,
    preferred_pro boolean,
    created_at timestamp without time zone
);


ALTER TABLE scheduling_dev.line_items_dev OWNER TO postgres;

--
-- TOC entry 668 (class 1259 OID 10937491)
-- Name: notes; Type: TABLE; Schema: scheduling_dev; Owner: postgres
--

CREATE TABLE scheduling_dev.notes (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    customer_id uuid,
    pro_id uuid,
    booking_id uuid,
    notes character varying,
    status character varying,
    staff_only_access boolean,
    created_at timestamp without time zone DEFAULT now()
);


ALTER TABLE scheduling_dev.notes OWNER TO postgres;

--
-- TOC entry 692 (class 1259 OID 10982142)
-- Name: preferences; Type: TABLE; Schema: scheduling_dev; Owner: postgres
--

CREATE TABLE scheduling_dev.preferences (
    business_id uuid NOT NULL,
    opt_in boolean DEFAULT true,
    created_at timestamp without time zone DEFAULT now()
);


ALTER TABLE scheduling_dev.preferences OWNER TO postgres;

--
-- TOC entry 670 (class 1259 OID 10937506)
-- Name: pro_schedule_booking; Type: TABLE; Schema: scheduling_dev; Owner: postgres
--

CREATE TABLE scheduling_dev.pro_schedule_booking (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    business_id uuid,
    pro_id uuid,
    schedule_id uuid,
    booking_id uuid,
    reschedule_booking_id uuid,
    created_at timestamp without time zone DEFAULT now()
);


ALTER TABLE scheduling_dev.pro_schedule_booking OWNER TO postgres;

--
-- TOC entry 669 (class 1259 OID 10937500)
-- Name: pro_schedule_service; Type: TABLE; Schema: scheduling_dev; Owner: postgres
--

CREATE TABLE scheduling_dev.pro_schedule_service (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    pro_id uuid,
    schedule_id uuid,
    service_id uuid,
    created_at timestamp without time zone DEFAULT now()
);


ALTER TABLE scheduling_dev.pro_schedule_service OWNER TO postgres;

--
-- TOC entry 660 (class 1259 OID 10936377)
-- Name: pros; Type: TABLE; Schema: scheduling_dev; Owner: postgres
--

CREATE TABLE scheduling_dev.pros (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    business_id uuid NOT NULL,
    profession character varying,
    first_name character varying,
    last_name character varying,
    phone character varying NOT NULL,
    email character varying,
    created_at timestamp without time zone DEFAULT now()
);


ALTER TABLE scheduling_dev.pros OWNER TO postgres;

--
-- TOC entry 688 (class 1259 OID 10971479)
-- Name: reminders; Type: TABLE; Schema: scheduling_dev; Owner: postgres
--

CREATE TABLE scheduling_dev.reminders (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    booking_id uuid,
    email boolean,
    sms boolean,
    created_at timestamp without time zone DEFAULT now(),
    execution_status character varying,
    creation_status boolean,
    type character varying,
    deleted boolean,
    error_reason character varying
);


ALTER TABLE scheduling_dev.reminders OWNER TO postgres;

--
-- TOC entry 667 (class 1259 OID 10937482)
-- Name: rescheduled_bookings; Type: TABLE; Schema: scheduling_dev; Owner: postgres
--

CREATE TABLE scheduling_dev.rescheduled_bookings (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    booking_id uuid,
    start_time timestamp without time zone,
    duration integer,
    status character varying,
    reschedule_initiated_by character varying,
    reschedule_reason character varying,
    created_at timestamp without time zone DEFAULT now()
);


ALTER TABLE scheduling_dev.rescheduled_bookings OWNER TO postgres;

--
-- TOC entry 661 (class 1259 OID 10937408)
-- Name: schedules; Type: TABLE; Schema: scheduling_dev; Owner: postgres
--

CREATE TABLE scheduling_dev.schedules (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    pro_id uuid,
    schedule jsonb,
    created_at timestamp without time zone DEFAULT now(),
    timezone character varying DEFAULT ''::character varying
);


ALTER TABLE scheduling_dev.schedules OWNER TO postgres;

--
-- TOC entry 1064 (class 1259 OID 11107721)
-- Name: service_logs; Type: TABLE; Schema: scheduling_dev; Owner: postgres
--

CREATE TABLE scheduling_dev.service_logs (
    id uuid,
    business_id uuid,
    name character varying,
    category character varying,
    description character varying,
    photo character varying,
    created_at timestamp without time zone,
    category_id uuid,
    deleted boolean DEFAULT false,
    primary_id integer NOT NULL,
    operation character varying,
    timestamp_ timestamp without time zone DEFAULT now()
);


ALTER TABLE scheduling_dev.service_logs OWNER TO postgres;

--
-- TOC entry 1063 (class 1259 OID 11107719)
-- Name: service_logs_primary_id_seq; Type: SEQUENCE; Schema: scheduling_dev; Owner: postgres
--

CREATE SEQUENCE scheduling_dev.service_logs_primary_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE scheduling_dev.service_logs_primary_id_seq OWNER TO postgres;

--
-- TOC entry 7519 (class 0 OID 0)
-- Dependencies: 1063
-- Name: service_logs_primary_id_seq; Type: SEQUENCE OWNED BY; Schema: scheduling_dev; Owner: postgres
--

ALTER SEQUENCE scheduling_dev.service_logs_primary_id_seq OWNED BY scheduling_dev.service_logs.primary_id;


--
-- TOC entry 663 (class 1259 OID 10937440)
-- Name: service_variations; Type: TABLE; Schema: scheduling_dev; Owner: postgres
--

CREATE TABLE scheduling_dev.service_variations (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    service_id uuid,
    name character varying,
    duration integer,
    price double precision,
    description character varying,
    photo character varying,
    created_at timestamp without time zone DEFAULT now(),
    deleted boolean DEFAULT false,
    pricing_type character varying DEFAULT 'FIXED'::character varying,
    price_end double precision
);


ALTER TABLE scheduling_dev.service_variations OWNER TO postgres;

--
-- TOC entry 662 (class 1259 OID 10937431)
-- Name: services; Type: TABLE; Schema: scheduling_dev; Owner: postgres
--

CREATE TABLE scheduling_dev.services (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    business_id uuid,
    name character varying,
    category character varying,
    description character varying,
    photo character varying,
    created_at timestamp without time zone DEFAULT now(),
    category_id uuid,
    deleted boolean DEFAULT false
);


ALTER TABLE scheduling_dev.services OWNER TO postgres;

--
-- TOC entry 1030 (class 1259 OID 11102079)
-- Name: sp_block_calendar; Type: TABLE; Schema: scheduling_dev; Owner: postgres
--

CREATE TABLE scheduling_dev.sp_block_calendar (
    business_id uuid,
    created_at timestamp without time zone DEFAULT now(),
    start_time timestamp without time zone,
    end_time timestamp without time zone,
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    description character varying,
    deleted boolean DEFAULT false
);


ALTER TABLE scheduling_dev.sp_block_calendar OWNER TO postgres;

--
-- TOC entry 7281 (class 2604 OID 11107476)
-- Name: category_logs primary_id; Type: DEFAULT; Schema: scheduling_dev; Owner: postgres
--

ALTER TABLE ONLY scheduling_dev.category_logs ALTER COLUMN primary_id SET DEFAULT nextval('scheduling_dev.category_logs_primary_id_seq'::regclass);


--
-- TOC entry 7284 (class 2604 OID 11107725)
-- Name: service_logs primary_id; Type: DEFAULT; Schema: scheduling_dev; Owner: postgres
--

ALTER TABLE ONLY scheduling_dev.service_logs ALTER COLUMN primary_id SET DEFAULT nextval('scheduling_dev.service_logs_primary_id_seq'::regclass);

--
-- TOC entry 7520 (class 0 OID 0)
-- Dependencies: 872
-- Name: booking_primary_id_seq; Type: SEQUENCE SET; Schema: scheduling_dev; Owner: postgres
--

SELECT pg_catalog.setval('scheduling_dev.booking_primary_id_seq', 1920, true);


--
-- TOC entry 7521 (class 0 OID 0)
-- Dependencies: 878
-- Name: business_logs_primary_id_seq; Type: SEQUENCE SET; Schema: scheduling_dev; Owner: postgres
--

SELECT pg_catalog.setval('scheduling_dev.business_logs_primary_id_seq', 772, true);


--
-- TOC entry 7522 (class 0 OID 0)
-- Dependencies: 1061
-- Name: category_logs_primary_id_seq; Type: SEQUENCE SET; Schema: scheduling_dev; Owner: postgres
--

SELECT pg_catalog.setval('scheduling_dev.category_logs_primary_id_seq', 2724, true);


--
-- TOC entry 7523 (class 0 OID 0)
-- Dependencies: 870
-- Name: line_item_logs_primary_id_seq; Type: SEQUENCE SET; Schema: scheduling_dev; Owner: postgres
--

SELECT pg_catalog.setval('scheduling_dev.line_item_logs_primary_id_seq', 1817, true);


--
-- TOC entry 7524 (class 0 OID 0)
-- Dependencies: 1063
-- Name: service_logs_primary_id_seq; Type: SEQUENCE SET; Schema: scheduling_dev; Owner: postgres
--

SELECT pg_catalog.setval('scheduling_dev.service_logs_primary_id_seq', 1, false);


--
-- TOC entry 7299 (class 2606 OID 10937471)
-- Name: bookings bookings_pkey; Type: CONSTRAINT; Schema: scheduling_dev; Owner: postgres
--

ALTER TABLE ONLY scheduling_dev.bookings
    ADD CONSTRAINT bookings_pkey PRIMARY KEY (id);


--
-- TOC entry 7287 (class 2606 OID 10936373)
-- Name: businesses businesses_pkey; Type: CONSTRAINT; Schema: scheduling_dev; Owner: postgres
--

ALTER TABLE ONLY scheduling_dev.businesses
    ADD CONSTRAINT businesses_pkey PRIMARY KEY (id);


--
-- TOC entry 7311 (class 2606 OID 10942277)
-- Name: categories categories_pkey; Type: CONSTRAINT; Schema: scheduling_dev; Owner: postgres
--

ALTER TABLE ONLY scheduling_dev.categories
    ADD CONSTRAINT categories_pkey PRIMARY KEY (id);


--
-- TOC entry 7319 (class 2606 OID 11107482)
-- Name: category_logs category_logs_pkey; Type: CONSTRAINT; Schema: scheduling_dev; Owner: postgres
--

ALTER TABLE ONLY scheduling_dev.category_logs
    ADD CONSTRAINT category_logs_pkey PRIMARY KEY (primary_id);


--
-- TOC entry 7297 (class 2606 OID 10937462)
-- Name: customers customer_pkey; Type: CONSTRAINT; Schema: scheduling_dev; Owner: postgres
--

ALTER TABLE ONLY scheduling_dev.customers
    ADD CONSTRAINT customer_pkey PRIMARY KEY (id);


--
-- TOC entry 7301 (class 2606 OID 10937477)
-- Name: line_items line_items_pkey; Type: CONSTRAINT; Schema: scheduling_dev; Owner: postgres
--

ALTER TABLE ONLY scheduling_dev.line_items
    ADD CONSTRAINT line_items_pkey PRIMARY KEY (id);


--
-- TOC entry 7305 (class 2606 OID 10937499)
-- Name: notes notes_pkey; Type: CONSTRAINT; Schema: scheduling_dev; Owner: postgres
--

ALTER TABLE ONLY scheduling_dev.notes
    ADD CONSTRAINT notes_pkey PRIMARY KEY (id);


--
-- TOC entry 7307 (class 2606 OID 10937505)
-- Name: pro_schedule_service pro_schedule_mapping_pkey; Type: CONSTRAINT; Schema: scheduling_dev; Owner: postgres
--

ALTER TABLE ONLY scheduling_dev.pro_schedule_service
    ADD CONSTRAINT pro_schedule_mapping_pkey PRIMARY KEY (id);


--
-- TOC entry 7309 (class 2606 OID 10937511)
-- Name: pro_schedule_booking pro_schedule_mapping_pkey1; Type: CONSTRAINT; Schema: scheduling_dev; Owner: postgres
--

ALTER TABLE ONLY scheduling_dev.pro_schedule_booking
    ADD CONSTRAINT pro_schedule_mapping_pkey1 PRIMARY KEY (id);


--
-- TOC entry 7289 (class 2606 OID 10936385)
-- Name: pros pros_pkey; Type: CONSTRAINT; Schema: scheduling_dev; Owner: postgres
--

ALTER TABLE ONLY scheduling_dev.pros
    ADD CONSTRAINT pros_pkey PRIMARY KEY (id);


--
-- TOC entry 7313 (class 2606 OID 10971484)
-- Name: reminders reminders_pkey; Type: CONSTRAINT; Schema: scheduling_dev; Owner: postgres
--

ALTER TABLE ONLY scheduling_dev.reminders
    ADD CONSTRAINT reminders_pkey PRIMARY KEY (id);


--
-- TOC entry 7303 (class 2606 OID 10937490)
-- Name: rescheduled_bookings rescheduled_bookings_pkey; Type: CONSTRAINT; Schema: scheduling_dev; Owner: postgres
--

ALTER TABLE ONLY scheduling_dev.rescheduled_bookings
    ADD CONSTRAINT rescheduled_bookings_pkey PRIMARY KEY (id);


--
-- TOC entry 7291 (class 2606 OID 10937417)
-- Name: schedules schedule_pkey; Type: CONSTRAINT; Schema: scheduling_dev; Owner: postgres
--

ALTER TABLE ONLY scheduling_dev.schedules
    ADD CONSTRAINT schedule_pkey PRIMARY KEY (id);


--
-- TOC entry 7315 (class 2606 OID 10975537)
-- Name: comms_content scheduling_dev_comms_pkey; Type: CONSTRAINT; Schema: scheduling_dev; Owner: postgres
--

ALTER TABLE ONLY scheduling_dev.comms_content
    ADD CONSTRAINT scheduling_dev_comms_pkey PRIMARY KEY (id);


--
-- TOC entry 7317 (class 2606 OID 10982147)
-- Name: preferences scheduling_dev_preferences_pkey; Type: CONSTRAINT; Schema: scheduling_dev; Owner: postgres
--

ALTER TABLE ONLY scheduling_dev.preferences
    ADD CONSTRAINT scheduling_dev_preferences_pkey PRIMARY KEY (business_id);


--
-- TOC entry 7321 (class 2606 OID 11107731)
-- Name: service_logs service_logs_pkey; Type: CONSTRAINT; Schema: scheduling_dev; Owner: postgres
--

ALTER TABLE ONLY scheduling_dev.service_logs
    ADD CONSTRAINT service_logs_pkey PRIMARY KEY (primary_id);


--
-- TOC entry 7295 (class 2606 OID 10937448)
-- Name: service_variations service_variations_pkey; Type: CONSTRAINT; Schema: scheduling_dev; Owner: postgres
--

ALTER TABLE ONLY scheduling_dev.service_variations
    ADD CONSTRAINT service_variations_pkey PRIMARY KEY (id);


--
-- TOC entry 7293 (class 2606 OID 10937439)
-- Name: services services_pkey; Type: CONSTRAINT; Schema: scheduling_dev; Owner: postgres
--

ALTER TABLE ONLY scheduling_dev.services
    ADD CONSTRAINT services_pkey PRIMARY KEY (id);


--
-- TOC entry 7351 (class 2620 OID 10993490)
-- Name: bookings booking_logs_trigger; Type: TRIGGER; Schema: scheduling_dev; Owner: postgres
--

CREATE TRIGGER booking_logs_trigger AFTER INSERT OR DELETE OR UPDATE ON scheduling_dev.bookings FOR EACH ROW EXECUTE FUNCTION scheduling_dev.booking_logs();


--
-- TOC entry 7350 (class 2620 OID 11003356)
-- Name: businesses business_logs_trigger; Type: TRIGGER; Schema: scheduling_dev; Owner: postgres
--

CREATE TRIGGER business_logs_trigger AFTER INSERT OR DELETE OR UPDATE ON scheduling_dev.businesses FOR EACH ROW EXECUTE FUNCTION scheduling_dev.business_logs();


--
-- TOC entry 7353 (class 2620 OID 11107491)
-- Name: categories category_logs_trigger; Type: TRIGGER; Schema: scheduling_dev; Owner: postgres
--

CREATE TRIGGER category_logs_trigger AFTER INSERT OR DELETE OR UPDATE ON scheduling_dev.categories FOR EACH ROW EXECUTE FUNCTION scheduling_dev.categories_logs();


--
-- TOC entry 7352 (class 2620 OID 10993468)
-- Name: line_items line_item_logs_trigger; Type: TRIGGER; Schema: scheduling_dev; Owner: postgres
--

CREATE TRIGGER line_item_logs_trigger AFTER INSERT OR DELETE OR UPDATE ON scheduling_dev.line_items FOR EACH ROW EXECUTE FUNCTION scheduling_dev.line_item_logs();


--
-- TOC entry 7327 (class 2606 OID 10937512)
-- Name: bookings bookings_business_id_fkey; Type: FK CONSTRAINT; Schema: scheduling_dev; Owner: postgres
--

ALTER TABLE ONLY scheduling_dev.bookings
    ADD CONSTRAINT bookings_business_id_fkey FOREIGN KEY (business_id) REFERENCES scheduling_dev.businesses(id) ON DELETE CASCADE;


--
-- TOC entry 7328 (class 2606 OID 10937517)
-- Name: bookings bookings_customer_id_fkey; Type: FK CONSTRAINT; Schema: scheduling_dev; Owner: postgres
--

ALTER TABLE ONLY scheduling_dev.bookings
    ADD CONSTRAINT bookings_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES scheduling_dev.customers(id) ON DELETE CASCADE;


--
-- TOC entry 7329 (class 2606 OID 10937522)
-- Name: bookings bookings_rescheduled_id_fkey; Type: FK CONSTRAINT; Schema: scheduling_dev; Owner: postgres
--

ALTER TABLE ONLY scheduling_dev.bookings
    ADD CONSTRAINT bookings_rescheduled_id_fkey FOREIGN KEY (rescheduled_id) REFERENCES scheduling_dev.rescheduled_bookings(id) ON DELETE CASCADE;


--
-- TOC entry 7347 (class 2606 OID 10975872)
-- Name: comms_content comms_copy_business_id_fkey; Type: FK CONSTRAINT; Schema: scheduling_dev; Owner: postgres
--

ALTER TABLE ONLY scheduling_dev.comms_content
    ADD CONSTRAINT comms_copy_business_id_fkey FOREIGN KEY (business_id) REFERENCES scheduling_dev.businesses(id) ON DELETE CASCADE;


--
-- TOC entry 7326 (class 2606 OID 10937545)
-- Name: customers customer_business_id_fkey; Type: FK CONSTRAINT; Schema: scheduling_dev; Owner: postgres
--

ALTER TABLE ONLY scheduling_dev.customers
    ADD CONSTRAINT customer_business_id_fkey FOREIGN KEY (business_id) REFERENCES scheduling_dev.businesses(id) ON DELETE CASCADE;


--
-- TOC entry 7330 (class 2606 OID 10937645)
-- Name: line_items line_items_booking_id_fkey; Type: FK CONSTRAINT; Schema: scheduling_dev; Owner: postgres
--

ALTER TABLE ONLY scheduling_dev.line_items
    ADD CONSTRAINT line_items_booking_id_fkey FOREIGN KEY (booking_id) REFERENCES scheduling_dev.bookings(id) ON DELETE CASCADE;


--
-- TOC entry 7331 (class 2606 OID 10937650)
-- Name: line_items line_items_pro_id_fkey; Type: FK CONSTRAINT; Schema: scheduling_dev; Owner: postgres
--

ALTER TABLE ONLY scheduling_dev.line_items
    ADD CONSTRAINT line_items_pro_id_fkey FOREIGN KEY (pro_id) REFERENCES scheduling_dev.pros(id) ON DELETE CASCADE;


--
-- TOC entry 7332 (class 2606 OID 10937655)
-- Name: line_items line_items_service_id_fkey; Type: FK CONSTRAINT; Schema: scheduling_dev; Owner: postgres
--

ALTER TABLE ONLY scheduling_dev.line_items
    ADD CONSTRAINT line_items_service_id_fkey FOREIGN KEY (service_id) REFERENCES scheduling_dev.services(id) ON DELETE CASCADE;


--
-- TOC entry 7333 (class 2606 OID 10937660)
-- Name: line_items line_items_service_variation_id_fkey; Type: FK CONSTRAINT; Schema: scheduling_dev; Owner: postgres
--

ALTER TABLE ONLY scheduling_dev.line_items
    ADD CONSTRAINT line_items_service_variation_id_fkey FOREIGN KEY (service_variation_id) REFERENCES scheduling_dev.service_variations(id);


--
-- TOC entry 7335 (class 2606 OID 10937688)
-- Name: notes notes_booking_id_fkey; Type: FK CONSTRAINT; Schema: scheduling_dev; Owner: postgres
--

ALTER TABLE ONLY scheduling_dev.notes
    ADD CONSTRAINT notes_booking_id_fkey FOREIGN KEY (booking_id) REFERENCES scheduling_dev.bookings(id) ON DELETE CASCADE;


--
-- TOC entry 7336 (class 2606 OID 10937678)
-- Name: notes notes_customer_id_fkey; Type: FK CONSTRAINT; Schema: scheduling_dev; Owner: postgres
--

ALTER TABLE ONLY scheduling_dev.notes
    ADD CONSTRAINT notes_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES scheduling_dev.customers(id) ON DELETE CASCADE;


--
-- TOC entry 7337 (class 2606 OID 10937683)
-- Name: notes notes_pro_id_fkey; Type: FK CONSTRAINT; Schema: scheduling_dev; Owner: postgres
--

ALTER TABLE ONLY scheduling_dev.notes
    ADD CONSTRAINT notes_pro_id_fkey FOREIGN KEY (pro_id) REFERENCES scheduling_dev.pros(id) ON DELETE CASCADE;


--
-- TOC entry 7341 (class 2606 OID 10937713)
-- Name: pro_schedule_booking pro_schedule_mapping_booking_id_fkey; Type: FK CONSTRAINT; Schema: scheduling_dev; Owner: postgres
--

ALTER TABLE ONLY scheduling_dev.pro_schedule_booking
    ADD CONSTRAINT pro_schedule_mapping_booking_id_fkey FOREIGN KEY (booking_id) REFERENCES scheduling_dev.bookings(id) ON DELETE CASCADE;


--
-- TOC entry 7342 (class 2606 OID 10937693)
-- Name: pro_schedule_booking pro_schedule_mapping_business_id_fkey; Type: FK CONSTRAINT; Schema: scheduling_dev; Owner: postgres
--

ALTER TABLE ONLY scheduling_dev.pro_schedule_booking
    ADD CONSTRAINT pro_schedule_mapping_business_id_fkey FOREIGN KEY (business_id) REFERENCES scheduling_dev.businesses(id) ON DELETE CASCADE;


--
-- TOC entry 7343 (class 2606 OID 10937698)
-- Name: pro_schedule_booking pro_schedule_mapping_pro_id_fkey; Type: FK CONSTRAINT; Schema: scheduling_dev; Owner: postgres
--

ALTER TABLE ONLY scheduling_dev.pro_schedule_booking
    ADD CONSTRAINT pro_schedule_mapping_pro_id_fkey FOREIGN KEY (pro_id) REFERENCES scheduling_dev.pros(id) ON DELETE CASCADE;


--
-- TOC entry 7344 (class 2606 OID 10937718)
-- Name: pro_schedule_booking pro_schedule_mapping_reschedule_booking_id_fkey; Type: FK CONSTRAINT; Schema: scheduling_dev; Owner: postgres
--

ALTER TABLE ONLY scheduling_dev.pro_schedule_booking
    ADD CONSTRAINT pro_schedule_mapping_reschedule_booking_id_fkey FOREIGN KEY (reschedule_booking_id) REFERENCES scheduling_dev.rescheduled_bookings(id) ON DELETE CASCADE;


--
-- TOC entry 7345 (class 2606 OID 10937703)
-- Name: pro_schedule_booking pro_schedule_mapping_schedule_id_fkey; Type: FK CONSTRAINT; Schema: scheduling_dev; Owner: postgres
--

ALTER TABLE ONLY scheduling_dev.pro_schedule_booking
    ADD CONSTRAINT pro_schedule_mapping_schedule_id_fkey FOREIGN KEY (schedule_id) REFERENCES scheduling_dev.schedules(id) ON UPDATE CASCADE;


--
-- TOC entry 7338 (class 2606 OID 10937723)
-- Name: pro_schedule_service pro_schedule_service_pro_id_fkey; Type: FK CONSTRAINT; Schema: scheduling_dev; Owner: postgres
--

ALTER TABLE ONLY scheduling_dev.pro_schedule_service
    ADD CONSTRAINT pro_schedule_service_pro_id_fkey FOREIGN KEY (pro_id) REFERENCES scheduling_dev.pros(id) ON DELETE CASCADE;


--
-- TOC entry 7339 (class 2606 OID 10937728)
-- Name: pro_schedule_service pro_schedule_service_schedule_id_fkey; Type: FK CONSTRAINT; Schema: scheduling_dev; Owner: postgres
--

ALTER TABLE ONLY scheduling_dev.pro_schedule_service
    ADD CONSTRAINT pro_schedule_service_schedule_id_fkey FOREIGN KEY (schedule_id) REFERENCES scheduling_dev.schedules(id) ON DELETE CASCADE;


--
-- TOC entry 7340 (class 2606 OID 10937733)
-- Name: pro_schedule_service pro_schedule_service_service_id_fkey; Type: FK CONSTRAINT; Schema: scheduling_dev; Owner: postgres
--

ALTER TABLE ONLY scheduling_dev.pro_schedule_service
    ADD CONSTRAINT pro_schedule_service_service_id_fkey FOREIGN KEY (service_id) REFERENCES scheduling_dev.services(id) ON DELETE CASCADE;


--
-- TOC entry 7322 (class 2606 OID 10936387)
-- Name: pros pros_business_id_fkey; Type: FK CONSTRAINT; Schema: scheduling_dev; Owner: postgres
--

ALTER TABLE ONLY scheduling_dev.pros
    ADD CONSTRAINT pros_business_id_fkey FOREIGN KEY (business_id) REFERENCES scheduling_dev.businesses(id) ON DELETE CASCADE;


--
-- TOC entry 7346 (class 2606 OID 10971485)
-- Name: reminders reminders_booking_id_fkey; Type: FK CONSTRAINT; Schema: scheduling_dev; Owner: postgres
--

ALTER TABLE ONLY scheduling_dev.reminders
    ADD CONSTRAINT reminders_booking_id_fkey FOREIGN KEY (booking_id) REFERENCES scheduling_dev.bookings(id) ON DELETE CASCADE;


--
-- TOC entry 7334 (class 2606 OID 10937738)
-- Name: rescheduled_bookings rescheduled_bookings_booking_id_fkey; Type: FK CONSTRAINT; Schema: scheduling_dev; Owner: postgres
--

ALTER TABLE ONLY scheduling_dev.rescheduled_bookings
    ADD CONSTRAINT rescheduled_bookings_booking_id_fkey FOREIGN KEY (booking_id) REFERENCES scheduling_dev.bookings(id) ON DELETE CASCADE;


--
-- TOC entry 7323 (class 2606 OID 10953959)
-- Name: schedules schedules_pro_id_fkey; Type: FK CONSTRAINT; Schema: scheduling_dev; Owner: postgres
--

ALTER TABLE ONLY scheduling_dev.schedules
    ADD CONSTRAINT schedules_pro_id_fkey FOREIGN KEY (pro_id) REFERENCES scheduling_dev.pros(id) ON DELETE CASCADE;


--
-- TOC entry 7325 (class 2606 OID 10953964)
-- Name: service_variations service_variations_service_id_fkey; Type: FK CONSTRAINT; Schema: scheduling_dev; Owner: postgres
--

ALTER TABLE ONLY scheduling_dev.service_variations
    ADD CONSTRAINT service_variations_service_id_fkey FOREIGN KEY (service_id) REFERENCES scheduling_dev.services(id) ON DELETE CASCADE;


--
-- TOC entry 7324 (class 2606 OID 11020429)
-- Name: services services_category_id_fkey; Type: FK CONSTRAINT; Schema: scheduling_dev; Owner: postgres
--

ALTER TABLE ONLY scheduling_dev.services
    ADD CONSTRAINT services_category_id_fkey FOREIGN KEY (category_id) REFERENCES scheduling_dev.categories(id) ON DELETE CASCADE;


--
-- TOC entry 7348 (class 2606 OID 11103064)
-- Name: sp_block_calendar sp_block_calendar_business_id_fkey; Type: FK CONSTRAINT; Schema: scheduling_dev; Owner: postgres
--

ALTER TABLE ONLY scheduling_dev.sp_block_calendar
    ADD CONSTRAINT sp_block_calendar_business_id_fkey FOREIGN KEY (business_id) REFERENCES scheduling_dev.businesses(id);


--
-- TOC entry 7349 (class 2606 OID 11103069)
-- Name: sp_block_calendar sp_block_calendar_business_id_fkey1; Type: FK CONSTRAINT; Schema: scheduling_dev; Owner: postgres
--

ALTER TABLE ONLY scheduling_dev.sp_block_calendar
    ADD CONSTRAINT sp_block_calendar_business_id_fkey1 FOREIGN KEY (business_id) REFERENCES scheduling_dev.businesses(id);


-- Completed on 2023-11-27 19:10:30

--
-- PostgreSQL database dump complete
--

