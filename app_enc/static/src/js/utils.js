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

function formatDateDDMMYYYY(date) {
  /**
   * return formato 'dd/mm/yyyy, HH:MM:SS'
   */
  const fecha = new Date(date);
  const year = fecha.getUTCFullYear();
  const month = String(fecha.getUTCMonth() + 1).padStart(2, '0');
  const day = String(fecha.getUTCDate()).padStart(2, '0');
  const hour = String(fecha.getUTCHours()).padStart(2, '0');
  const minute = String(fecha.getUTCMinutes()).padStart(2, '0');
  const second = String(fecha.getUTCSeconds()).padStart(2, '0');
  return `${day}/${month}/${year}, ${hour}:${minute}:${second}`;
};

const getDateGMT = (dateUTC) => {
  /**
   * @params 2024-03-04
   * @return Mon Mar 04 2024 00:00:00 GMT-0500 (hora estándar de Perú)
   */
  const fecha = new Date(dateUTC);
  const fechaUTC = fecha.setHours(fecha.getHours() + 5); // Por que al cambiar a la hora local le resta 5 horas ya que Date es UTC
  return new Date(fechaUTC)
};

const isObjectEmpty = (objectName) => {
    /**
     * @params objectName {} objeto de primer nivel
     */
    return (
      objectName &&
      Object.keys(objectName).length === 0 &&
      objectName.constructor === Object
    );
  };

const isSomeValueEmpty = (obj) => {
    /**
     * @param obj {} objeto de primer nivel
     */
    return Object.values(obj).some(value => {
      return value === ''
    });
  };

const capitalizeFirstLetter = (string) => {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

const formatCurrency = (value) => {
  return value.toLocaleString('es-PE', { style: 'currency', currency: 'PEN' });
};

export {convertirFormatoFecha, isObjectEmpty, isSomeValueEmpty, capitalizeFirstLetter, formatCurrency, formatDateDDMMYYYY, getDateGMT};