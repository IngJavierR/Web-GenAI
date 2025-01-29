export class ResumeResponse {
    id: number = 0;
    nombre: string = "";
    apellido: string = "";
    fecha_nacimiento: string | null  = "";
    email: string = "";
    telefono: string | null = "";
    direccion: string | null = "";
    fecha_ingreso: string | null = "";
    descripcion: string | null = "";
    experiencia: Experiencia[];
    conocimientos: Conocimiento[];
    idiomas: Idioma[];
    certificaciones: Certificacion[];
    herramientas: Herramienta[];
    educacion: Educacion[];
  
    constructor(data?: Partial<ResumeResponse>) {
      Object.assign(this, data);
      this.experiencia = data?.experiencia?.map(e => new Experiencia(e)) || [];
      this.conocimientos = data?.conocimientos?.map(c => new Conocimiento(c)) || [];
      this.idiomas = data?.idiomas?.map(i => new Idioma(i)) || [];
      this.certificaciones = data?.certificaciones?.map(c => new Certificacion(c)) || [];
      this.herramientas = data?.herramientas?.map(h => new Herramienta(h)) || [];
      this.educacion = data?.educacion?.map(e => new Educacion(e)) || [];
    }
  }
  
  export class Experiencia {
    id: number = 0;
    empresa: string = "";
    puesto: string | null = "";
    fecha_inicio: string | null = "";
    fecha_fin: string | null = "";
    descripcion: string | null = "";
    actividades: Actividad[];
  
    constructor(data?: Partial<Experiencia>) {
      Object.assign(this, data);
      this.actividades = data?.actividades?.map(a => new Actividad(a)) || [];
    }
  }
  
  export class Actividad {
    id: number = 0;
    descripcion: string = "";
  
    constructor(data?: Partial<Actividad>) {
      Object.assign(this, data);
    }
  }
  
  export class Conocimiento {
    id: number = 0;
    conocimiento: string = "";
    nivel: string | null = "";
  
    constructor(data?: Partial<Conocimiento>) {
      Object.assign(this, data);
    }
  }
  
  export class Idioma {
    id: number = 0;
    idioma: string = "";
    nivel: string = "";
  
    constructor(data?: Partial<Idioma>) {
      Object.assign(this, data);
    }
  }
  
  export class Certificacion {
    id: number = 0;
    certificacion: string = "";
    institucion: string | null = "";
    fecha_obtencion: string | null = "";
    fecha_expiracion: string | null = "";
  
    constructor(data?: Partial<Certificacion>) {
      Object.assign(this, data);
    }
  }
  
  export class Herramienta {
    id: number = 0;
    herramienta: string = "";
    nivel: string | null = "";
  
    constructor(data?: Partial<Herramienta>) {
      Object.assign(this, data);
    }
  }
  
  export class Educacion {
    id: number = 0;
    institucion: string = "";
    titulo: string | null = "";
    fecha_inicio: string | null = "";
    fecha_fin: string | null = "";
  
    constructor(data?: Partial<Educacion>) {
      Object.assign(this, data);
    }
  }
  