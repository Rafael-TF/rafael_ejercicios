
-- Consultas SELECT

/*
- ¿Que bootcamp tiene más estudiantes?
- ¿Cuantos bootcamps no tienen estudiantes?
- ¿Que estudiantes tienen más asistencias y cuales tiene menos?
- ¿Que modulo tiene mas puntuación de media y cual tiene menos puntuación de media?
- ¿Qué bootcamp tiene mayor puntuación de media?
- ¿Qué bootcamp tiene mas asistencias y cual tiene menos asistencias? Los bootcamps sin estudiantes no cuentan.
- ¿Qué día tiene el mayor número de asistencias y cual tiene el menor número de asistencias?
- ¿Cuales bootcamps le dan 10 al modulo de **Machine Learning**?
- Muestra los 10 estudiantes que tenga más asistencias (_subqueries_).
*/

USE bootcamps;

-- ¿Que bootcamp tiene más estudiantes?
SELECT b.bootcamp AS nombre_bootcamp,
COUNT(e.estudiante_id) AS numero_estudiantes
FROM bootcamps b
INNER JOIN estudiantes e ON e.bootcamp_id = b.bootcamp_id
GROUP BY b.bootcamp
ORDER BY COUNT(e.estudiante_id) DESC;

-- ¿Cuantos bootcamps no tienen estudiantes?
SELECT b.bootcamp AS nombre_bootcamp,
COUNT(e.estudiante_id) AS numero_estudiantes
FROM bootcamps b
LEFT JOIN estudiantes e ON e.bootcamp_id = b.bootcamp_id
GROUP BY b.bootcamp
HAVING COUNT(e.estudiante_id) = 0;

-- ¿Que estudiantes tienen más asistencias y cuales tiene menos?
--MAYOR ASISTENCIA
SELECT a.estudiante_id, SUM(a.asistencia)
FROM asistencias a
GROUP BY a.estudiante_id
ORDER BY SUM(a.asistencia) DESC;

--MENOR ASISTENCIA
SELECT a.estudiante_id, SUM(a.asistencia)
FROM asistencias a
GROUP BY a.estudiante_id
ORDER BY SUM(a.asistencia);

-- ¿Que modulo tiene mas puntuación de media y cual tiene menos puntuación de media?
SELECT 
    m.nombre,
    ROUND(AVG(mb.puntuacion), 2) AS puntuacion_media
FROM 
    modulos m
JOIN 
   modulo_bootcamps mb ON m.modulo_id = mb.modulo_id
GROUP BY 
    m.nombre
ORDER BY 
    puntuacion_media DESC;

-- ¿Qué bootcamp tiene mayor puntuación de media?
SELECT 
    b.bootcamp,
    ROUND(AVG(mb.puntuacion), 2) AS puntuacion_media
FROM 
    bootcamps b
JOIN 
   modulo_bootcamp mb ON b.bootcamp_id = mb.bootcamp_id
GROUP BY 
    b.bootcamp
ORDER BY 
    puntuacion_media DESC

-- ¿Qué bootcamp tiene mas asistencias y cual tiene menos asistencias? Los bootcamps sin estudiantes no cuentan.
-- BOOTCAMP CON MAYOR NUMERO DE ASISTENCIAS
SELECT
    b.bootcamp, 
    SUM(a.asistencia) AS total_asistencias
FROM
    asistencias a
JOIN 
    estudiantes e ON a.estudiante_id = e.estudiante_id
JOIN 
    bootcamps b ON e.bootcamp_id = b.bootcamp_id
GROUP BY
    b.bootcamp
HAVING 
    total_asistencias > 0
ORDER BY
    total_asistencias DESC;

-- BOOTCAMP CON MENOR NUMERO DE ASISTENCIAS
SELECT
    b.bootcamp, 
    SUM(a.asistencia) AS total_asistencias
FROM
    asistencias a
JOIN 
    estudiantes e ON a.estudiante_id = e.estudiante_id
JOIN 
    bootcamps b ON e.bootcamp_id = b.bootcamp_id
GROUP BY
    b.bootcamp
HAVING 
    total_asistencias > 0
ORDER BY
    total_asistencias;

-- ¿Qué día tiene el mayor número de asistencias y cual tiene el menor número de asistencias?
-- DIA CON MAYOR NUMERO DE ASISTENCIA
SELECT
    a.fecha,
    SUM(a.asistencia) AS total_asistencias
FROM
    asistencias a
GROUP BY
    a.fecha
ORDER BY
    total_asistencias DESC
LIMIT 1;

-- DIA CON MENOR NUMERO DE ASISTENCIA
SELECT
    a.fecha,
    SUM(a.asistencia) AS total_asistencias
FROM
    asistencias a
GROUP BY
    a.fecha
ORDER BY
    total_asistencias
LIMIT 1;

-- ¿Cuales bootcamps le dan 10 al modulo de **Machine Learning**?
SELECT 
    b.bootcamp AS bootcamp_nombre,
    m.nombre, 
    mb.puntuacion
FROM 
    modulos m
JOIN 
    modulo_bootcamps mb ON m.modulo_id = mb.modulo_id
JOIN 
    bootcamps b ON mb.bootcamp_id = b.bootcamp_id
WHERE 
    m.nombre = 'Machine Learning' AND 
    mb.puntuacion = 10;

-- Muestra los 10 estudiantes que tenga más asistencias (_subqueries_).
SELECT
    e.estudiante_id,
    e.nombre,
    e.apellido,
    COUNT(a.estudiante_id) AS total_asistencias
FROM
    estudiantes e
JOIN
    asistencias a ON e.estudiante_id = a.estudiante_id
GROUP BY
    e.estudiante_id
ORDER BY
    total_asistencias DESC
LIMIT 10;


SELECT 
    e.*, 
    sub.total_asistencias
FROM 
    estudiantes e
JOIN 
    (
        SELECT 
            estudiante_id, 
            COUNT(*) AS total_asistencias
        FROM 
            asistencias
        GROUP BY 
            estudiante_id
        ORDER BY 
            total_asistencias DESC
        LIMIT 10
    ) AS sub
ON 
    e.estudiante_id = sub.estudiante_id;

