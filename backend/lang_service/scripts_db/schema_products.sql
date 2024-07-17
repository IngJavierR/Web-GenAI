CREATE TABLE Categorias (
    id_categoria SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT
);

CREATE TABLE Proveedores (
    id_proveedor SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    contacto VARCHAR(100),
    telefono VARCHAR(30),
    email VARCHAR(100)
);

CREATE TABLE Productos (
    id_producto SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10, 2) NOT NULL,
    url VARCHAR(250) NOT NULL,
    id_categoria INT NOT NULL,
    id_proveedor INT NOT NULL,
    FOREIGN KEY (id_categoria)
        REFERENCES Categorias (id_categoria)
        ON DELETE CASCADE,
    FOREIGN KEY (id_proveedor)
        REFERENCES Proveedores (id_proveedor)
        ON DELETE CASCADE
);

CREATE TABLE Inventario (
    id_inventario SERIAL PRIMARY KEY,
    id_producto INT NOT NULL,
    cantidad INT NOT NULL,
    fecha_entrada DATE NOT NULL,
    fecha_salida DATE,
    ubicacion VARCHAR(100),
    FOREIGN KEY (id_producto)
        REFERENCES Productos (id_producto)
        ON DELETE CASCADE
);
