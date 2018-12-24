CREATE DATABASE consumption;

\connect consumption

CREATE TABLE public.probes
(
    id SERIAL PRIMARY KEY,
    label text,
    description text,
    realvirtual boolean,
    formula text,
    tariff_id INT
);
COMMENT ON COLUMN probes.id is 'probe internal identifier';
COMMENT ON COLUMN probes.label is 'probe external identifier';
COMMENT ON COLUMN probes.realvirtual is 'Real probe or virtual by applying formula';
COMMENT ON COLUMN probes.formula is 'Formula to apply to the real probes to get the virtual one';
\copy public.probes(label,description,realvirtual,formula) FROM '/docker-entrypoint-initdb.d/probes.csv' DELIMITER ',' CSV HEADER;


CREATE TABLE public.tariff
(
    id SERIAL PRIMARY KEY,
    name text,
    valley NUMERIC(8,7),
    peak   NUMERIC(8,7)
);
COMMENT ON COLUMN tariff.name is 'Tariff name';
COMMENT ON COLUMN tariff.valley is 'Price in valley time';
COMMENT ON COLUMN tariff.peak is   'Price in peak time';
\copy public.tariff(name,valley,peak) FROM '/docker-entrypoint-initdb.d/tariff.csv' DELIMITER ',' CSV HEADER;

CREATE TABLE public.taxes
(
    id SERIAL PRIMARY KEY,
    name text,
    relabs boolean,
    value NUMERIC(8,5) 
);
COMMENT ON COLUMN taxes.name is 'Taxes name';
COMMENT ON COLUMN taxes.relabs is 'Tax relative (%) or absolute (fix quantity)';
COMMENT ON COLUMN taxes.value is 'Amount to tax';
\copy public.taxes(name,relabs,value) FROM '/docker-entrypoint-initdb.d/taxes.csv' DELIMITER ',' CSV HEADER;

CREATE TABLE public.data
(
  probe_id INT,
  time TIMESTAMP,
  vrms NUMERIC(5,2),
  irms NUMERIC(4,2),
  power_aparent NUMERIC(7,2),
  power_active NUMERIC(7,2),
  power_reactive_ind NUMERIC(7,2),
  power_reactive_cap NUMERIC(7,2),
  frequency NUMERIC(4,2),
  energy_active NUMERIC(12,2),
  energy_reactive_ind NUMERIC(12,2),
  energy_reactive_cap NUMERIC(12,2),
  energy NUMERIC(7,2),
  price NUMERIC(11,9)
);
COMMENT ON COLUMN data.probe_id is 'Probe id from the probes table';
COMMENT ON COLUMN data.energy is 'Amount of energy since the last sample';
COMMENT ON COLUMN data.price  is 'Amount of money since the last sample';
CREATE INDEX dataidx on data(probe_id,time);
