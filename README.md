# Archivos importantes

Para hacer funcionar el bot, en el contendor Docker o simplemente el archivo Python, se necesitan añadir dos archivos. Son el '.env' y 'admin.json'. El primer archivo es necesario para que el bot de Discord obtenga su token y el segundo (opcional) es para hacer uso de las funciones de control reload o restart.

Ambos archivos **deben** estar tanto en el **directorio raíz** como en la **carpeta docker**.

## .ENV

En él se guarda el token del bot. Sin él, el bot no funcionará. Simplemente, hay que añadir un archivo con nombre '.env' y añadirle lo siguiente:

    DISCORD_TOKEN="XXX"

Donde XXX será vuestro token.

## admin.json

En este archivo estarán los ID de usuarios que podrán hacer uso de los comandos de administración del bot. El JSON debe ser una lista de ID en formato numérico tal como:

    [
        1234,
        5678
    ]

Sustituís los números puestos por vuestros ID de usuario de Discord. Para obtenerlos deberéis activar las opciones de desarrolladores en Discord y luego al hacer clic derecho sobre cualquier elemento de Discord os permite copiar el ID.