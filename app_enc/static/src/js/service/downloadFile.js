import axios from "axios";

const downloadNotaTxt = async (nroNotaCredito) => {
    const nroNotaCreditoTxt = `${nroNotaCredito}.txt`
    try {
        const response = await axios.get(`/nota_credito/download/${nroNotaCreditoTxt}`, {
            responseType: 'blob', // Especifica que esperamos una respuesta de tipo Blob
        });

        // Crear un objeto Blob con el contenido de la respuesta
        const blob = new Blob([response.data], { type: 'text/plain' });

        // Crear una URL del Blob
        const url = window.URL.createObjectURL(blob);

        // Crear un enlace <a> para iniciar la descarga
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', nroNotaCreditoTxt);

        // Simular un clic en el enlace para iniciar la descarga
        document.body.appendChild(link);
        link.click();

        // Limpiar la URL del Blob
        window.URL.revokeObjectURL(url);
        document.body.removeChild(link);
    } catch (error) {
        console.error(`Error al descargar el archivo: ${nroNotaCreditoTxt}`)
        throw new Error( `Error al descargar el archivo: ${nroNotaCreditoTxt}`);
    }
}

export {downloadNotaTxt};