class EmpleadoSerializers(serializers.ModelSerializer):
    asignacion = serializers.SerializerMethodField()
    asignacion_nombre = serializers.SerializerMethodField()
    cod_convenio = serializers.SerializerMethodField()
    convenio_descripcion = serializers.SerializerMethodField()
    en_proceso_baja = serializers.SerializerMethodField()

    def get_asignacion(self, obj):
        asignacion = obj.get_asignacion()
        codigo = asignacion.cod_estructura_desempenio.cod_estructura_real if asignacion is not None else None
        return codigo

    def get_asignacion_nombre(self, obj):
        asignacion = obj.get_asignacion()
        descripcion = asignacion.cod_estructura_desempenio.descripcion if asignacion is not None else None
        return descripcion

    def get_en_proceso_baja(self, obj):
        en_proceso_baja = obj.get_en_proceso_baja()
        return en_proceso_baja

    def get_cod_convenio(self, obj):
        asignacion = obj.get_asignacion()
        cod_convenio = asignacion.cod_convenio.cod_convenio if asignacion is not None else None
        return cod_convenio

    def get_convenio_descripcion(self, obj):
        asignacion = obj.get_asignacion()
        descripcion = asignacion.cod_convenio.descripcion if asignacion is not None else None
        return descripcion

    class Meta:
        model = Empleado
        fields = ('cuil',
                  'sexo',
                  'apellido',
                  'nombre',
                  'cod_tipo_doc',
                  'cod_estado_civil',
                  'nro_documento',
                  'cod_tipo_nacionalidad',
                  'cod_pais_nacimiento',
                  'fecha_nacimiento',
                  'lugar_nacimiento',
                  'legajo',
                  'legajo_anterior',
                  'fecha_ingreso',
                  'fecha_antiguedad',
                  'fecha_vacaciones',
                  'pasivo',
                  'ubicacion_legajo',
                  'fecha_confirmacion',
                  'id_transaccion',
                  'fecha_transaccion',
                  'cod_tipo_unidad',
                  'cod_unidad',
                  'cod_usuario',
                  'foto',
                  'antiguedad',
                  'acceso_gerencial',
                  'fecha_acceso_gerencial',
                  'nro_recibo',
                  'cod_tipo_unidad_ger',
                  'cod_unidad_ger',
                  'cod_usuario_ger',
                  'proc_otro_org',
                  'fecha_ini_nac',
                  'fecha_antiguedad_jub',
                  'cod_funcionario',
                  'cod_tratamiento',
                  'cod_nacionalidad',
                  'cod_prov_nacimiento',
                  'fecha_antiguedad_afin',
                  'asignacion',
                  'asignacion_nombre',
                  'cod_convenio',
                  'convenio_descripcion',
                  'en_proceso_baja')
