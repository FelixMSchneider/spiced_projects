-- this is done to get ISO Country codes into the database in order to be able to plot results on a map --
\c northwind
CREATE TABLE translator(
c_id integer,
country VARCHAR(100),
country_code VARCHAR(5));
\copy translator FROM '/home/felix/spiced/05_week/data/northwind_data_clean/translator.csv' DELIMITER ',' CSV HEADER;

