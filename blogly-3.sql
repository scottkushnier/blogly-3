--
-- PostgreSQL database dump
--

-- Dumped from database version 14.9 (Ubuntu 14.9-0ubuntu0.22.04.1)
-- Dumped by pg_dump version 14.9 (Ubuntu 14.9-0ubuntu0.22.04.1)

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: posts; Type: TABLE; Schema: public; Owner: kushnier
--

CREATE TABLE public.posts (
    id integer NOT NULL,
    title character varying(100) NOT NULL,
    content text,
    created_at timestamp without time zone NOT NULL,
    user_id integer
);


ALTER TABLE public.posts OWNER TO kushnier;

--
-- Name: posts_id_seq; Type: SEQUENCE; Schema: public; Owner: kushnier
--

CREATE SEQUENCE public.posts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.posts_id_seq OWNER TO kushnier;

--
-- Name: posts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kushnier
--

ALTER SEQUENCE public.posts_id_seq OWNED BY public.posts.id;


--
-- Name: posttags; Type: TABLE; Schema: public; Owner: kushnier
--

CREATE TABLE public.posttags (
    post_id integer NOT NULL,
    tag_id integer NOT NULL
);


ALTER TABLE public.posttags OWNER TO kushnier;

--
-- Name: tags; Type: TABLE; Schema: public; Owner: kushnier
--

CREATE TABLE public.tags (
    id integer NOT NULL,
    name character varying(30) NOT NULL
);


ALTER TABLE public.tags OWNER TO kushnier;

--
-- Name: tags_id_seq; Type: SEQUENCE; Schema: public; Owner: kushnier
--

CREATE SEQUENCE public.tags_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tags_id_seq OWNER TO kushnier;

--
-- Name: tags_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kushnier
--

ALTER SEQUENCE public.tags_id_seq OWNED BY public.tags.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: kushnier
--

CREATE TABLE public.users (
    id integer NOT NULL,
    first_name character varying(50) NOT NULL,
    last_name character varying(50) NOT NULL,
    image_url character varying(100)
);


ALTER TABLE public.users OWNER TO kushnier;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: kushnier
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO kushnier;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kushnier
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: posts id; Type: DEFAULT; Schema: public; Owner: kushnier
--

ALTER TABLE ONLY public.posts ALTER COLUMN id SET DEFAULT nextval('public.posts_id_seq'::regclass);


--
-- Name: tags id; Type: DEFAULT; Schema: public; Owner: kushnier
--

ALTER TABLE ONLY public.tags ALTER COLUMN id SET DEFAULT nextval('public.tags_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: kushnier
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: posts; Type: TABLE DATA; Schema: public; Owner: kushnier
--

COPY public.posts (id, title, content, created_at, user_id) FROM stdin;
1	done work	Yabba Dabba Doo!	2024-01-10 12:33:34	1
2	help!	How do you stop this crazy thing?	2024-01-10 12:33:59	1
3	Hi	Hiya Fred..	2024-01-10 12:34:19	2
4	Hi Betty	What chu up to Betty?	2024-01-10 13:06:47	2
12	everything	it's everything	2024-01-10 14:22:08	1
13	just sad	just sad	2024-01-10 14:22:19	1
14	It's stupid	OK. I'm stupid.	2024-01-10 14:25:59	2
15	dishes	There are many dirty dishes.	2024-01-10 15:41:59	3
16	Dishes	Time to do the dishes..	2024-01-10 15:44:53	2
\.


--
-- Data for Name: posttags; Type: TABLE DATA; Schema: public; Owner: kushnier
--

COPY public.posttags (post_id, tag_id) FROM stdin;
14	2
3	1
15	2
1	6
2	1
2	4
16	2
4	1
4	6
12	1
12	6
12	4
12	2
\.


--
-- Data for Name: tags; Type: TABLE DATA; Schema: public; Owner: kushnier
--

COPY public.tags (id, name) FROM stdin;
4	loony
1	funny
2	stupid
6	happy
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: kushnier
--

COPY public.users (id, first_name, last_name, image_url) FROM stdin;
1	Fred	Flintstone	images/fred.jpg
2	Barney	Rubble	images/barney.jpg
3	Wilma	Flintstone	images/img.jpg
\.


--
-- Name: posts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: kushnier
--

SELECT pg_catalog.setval('public.posts_id_seq', 16, true);


--
-- Name: tags_id_seq; Type: SEQUENCE SET; Schema: public; Owner: kushnier
--

SELECT pg_catalog.setval('public.tags_id_seq', 6, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: kushnier
--

SELECT pg_catalog.setval('public.users_id_seq', 3, true);


--
-- Name: posts posts_pkey; Type: CONSTRAINT; Schema: public; Owner: kushnier
--

ALTER TABLE ONLY public.posts
    ADD CONSTRAINT posts_pkey PRIMARY KEY (id);


--
-- Name: posttags posttags_pkey; Type: CONSTRAINT; Schema: public; Owner: kushnier
--

ALTER TABLE ONLY public.posttags
    ADD CONSTRAINT posttags_pkey PRIMARY KEY (post_id, tag_id);


--
-- Name: tags tags_pkey; Type: CONSTRAINT; Schema: public; Owner: kushnier
--

ALTER TABLE ONLY public.tags
    ADD CONSTRAINT tags_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: kushnier
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: posts posts_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: kushnier
--

ALTER TABLE ONLY public.posts
    ADD CONSTRAINT posts_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: posttags posttags_post_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: kushnier
--

ALTER TABLE ONLY public.posttags
    ADD CONSTRAINT posttags_post_id_fkey FOREIGN KEY (post_id) REFERENCES public.posts(id);


--
-- Name: posttags posttags_tag_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: kushnier
--

ALTER TABLE ONLY public.posttags
    ADD CONSTRAINT posttags_tag_id_fkey FOREIGN KEY (tag_id) REFERENCES public.tags(id);


--
-- PostgreSQL database dump complete
--

