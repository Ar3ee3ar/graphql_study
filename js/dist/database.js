// src/database.ts
import dotenv from 'dotenv';
import { createPool } from 'mysql2/promise';
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
    host: process.env.db_host,
    port: parseInt(process.env.db_port || '3306', 10),
    user: process.env.db_user,
    password: process.env.db_password || '',
    database: process.env.db_database,
    waitForConnections: true,
    connectionLimit: 10,
    queueLimit: 0
};
console.log(connectionOptions);
// create connection pool
export const pool = createPool(connectionOptions);
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
//# sourceMappingURL=database.js.map