PGDMP     .                    {            MentCare    14.6    15.2 	    �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    16402    MentCare    DATABASE     v   CREATE DATABASE "MentCare" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.UTF-8';
    DROP DATABASE "MentCare";
                postgres    false                        2615    16404    Security    SCHEMA        CREATE SCHEMA "Security";
    DROP SCHEMA "Security";
                postgres    false                        2615    2200    public    SCHEMA     2   -- *not* creating schema, since initdb creates it
 2   -- *not* dropping schema, since initdb creates it
                postgres    false            �           0    0    SCHEMA public    ACL     Q   REVOKE USAGE ON SCHEMA public FROM PUBLIC;
GRANT ALL ON SCHEMA public TO PUBLIC;
                   postgres    false    5            �            1259    16405    login    TABLE     b   CREATE TABLE "Security".login (
    username character varying,
    password character varying
);
    DROP TABLE "Security".login;
       Security         heap    postgres    false    6            �          0    16405    login 
   TABLE DATA           7   COPY "Security".login (username, password) FROM stdin;
    Security          postgres    false    210   d       �   �   x�5�I�   �u��5��֒�RK�g��68c3$&�o�?��_���F��*HU�D���ФnL_ӡ������}c�v���Z��~O�� l/�"(q���$j�D���@�7��Vd�U5��-M���m�9��A�C�]b���pR�q���l[Fϟu���XCۓ�J�a���57�� �_@�     