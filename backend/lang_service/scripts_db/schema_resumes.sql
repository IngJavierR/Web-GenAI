-- Creación de tablas principales
CREATE TABLE Consultores (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    fecha_nacimiento DATE,
    email VARCHAR(100) UNIQUE NOT NULL,
    telefono VARCHAR(100),
    direccion VARCHAR(255),
    fecha_ingreso DATE,
    descripcion TEXT
);

CREATE TABLE Experiencia_Laboral (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    consultor_id INT REFERENCES Consultores(id),
    empresa VARCHAR(100) NOT NULL,
    puesto VARCHAR(100),
    fecha_inicio DATE,
    fecha_fin DATE,
    descripcion TEXT
);

CREATE TABLE Actividades (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    experiencia_id INT REFERENCES Experiencia_Laboral(id),
    descripcion TEXT
);

CREATE TABLE Conocimientos_Tecnicos (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    consultor_id INT REFERENCES Consultores(id),
    conocimiento VARCHAR(100) NOT NULL,
    nivel VARCHAR(100)
);

CREATE TABLE Idiomas (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    consultor_id INT REFERENCES Consultores(id),
    idioma VARCHAR(100) NOT NULL,
    nivel VARCHAR(100)
);

CREATE TABLE Certificaciones (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    consultor_id INT REFERENCES Consultores(id),
    certificacion VARCHAR(100) NOT NULL,
    institucion VARCHAR(100),
    fecha_obtencion DATE,
    fecha_expiracion DATE
);

CREATE TABLE Herramientas (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    consultor_id INT REFERENCES Consultores(id),
    herramienta VARCHAR(100) NOT NULL,
    nivel VARCHAR(100)
);

CREATE TABLE Educacion (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    consultor_id INT REFERENCES Consultores(id),
    institucion VARCHAR(100) NOT NULL,
    titulo VARCHAR(100),
    fecha_inicio DATE,
    fecha_fin DATE
);

-- Creación de tablas auxiliares (catálogos)
CREATE TABLE Niveles_Conocimiento (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nivel VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE Niveles_Idiomas (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nivel VARCHAR(100) UNIQUE NOT NULL
);
