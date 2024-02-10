function convertirFormatoFecha(fechaString) {
    /**
     * return formato '%Y-%m-%dT%H:%M:%S.%fZ'
     */
    const fecha = new Date(fechaString);
    const year = fecha.getUTCFullYear();
    const month = String(fecha.getUTCMonth() + 1).padStart(2, '0');
    const day = String(fecha.getUTCDate()).padStart(2, '0');
    const hour = String(fecha.getUTCHours()).padStart(2, '0');
    const minute = String(fecha.getUTCMinutes()).padStart(2, '0');
    const second = String(fecha.getUTCSeconds()).padStart(2, '0');
    const millisecond = String(fecha.getUTCMilliseconds()).padStart(3, '0');
    const formatoFinal = `${year}-${month}-${day}T${hour}:${minute}:${second}.${millisecond}Z`;
    return formatoFinal;
};

export default convertirFormatoFecha;