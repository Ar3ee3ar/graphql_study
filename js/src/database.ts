// src/database.ts
import dotenv from 'dotenv';
import {createPool, type Pool} from 'mysql2/promise';

// read env file
dotenv.config();

// interface db_detail{
//     host: string,
//     port: number,
//     user: string,
//     password: string,
//     database: string,
//     waitForConnections: boolean,
//     connectionLimit: number,
//     queueLimit: number
// }

const connectionOptions = {
    host: process.env.db_host as string,
    port: parseInt(process.env.db_port || '3306',10) as number,
    user: process.env.db_user as string,
    password: process.env.db_password || '' as string,
    database: process.env.db_database as string,
    waitForConnections: true,
    connectionLimit: 10,
    queueLimit: 0
};

console.log(connectionOptions);

// create connection pool
export const pool: Pool = createPool(connectionOptions);

// test connection
// pool.getConnection((err, connection) => {
//     if(err){
//         console.error('Error connection to the database:', err.message);
//         return;
//     }
//     console.log('Connected to the MySQL server successfully');
//     connection.release();
// })

// export {
//     pool
// };