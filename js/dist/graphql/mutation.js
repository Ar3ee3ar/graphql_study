import { GraphQLObjectType, GraphQLSchema, GraphQLInt, GraphQLString, GraphQLList } from "graphql";
// const {graphqlHTTP} = require("express-graphql");
// import {graphqlHTTP} from "express-graphql"
import { UserType } from '../graphql/schema.js';
// import {pool} from '../database.js';
import { mapUser } from "./utils.js";
export const Mutation = new GraphQLObjectType({
    name: "Mutation",
    fields: {
        createUser: {
            type: UserType,
            args: {
                id: { type: GraphQLInt },
                firstName: { type: GraphQLString },
                lastName: { type: GraphQLString },
                email: { type: GraphQLString },
                password: { type: GraphQLString }
            },
            // partial - constructs a new type with all of the properties from the original Type set to optional
            // resolve(parent: unknown, args: Partial<Users>): Users {
            //     const newUser: Users = {
            //         id: userData.length + 1,
            //         firstName: args.firstName || '',
            //         lastName: args.lastName || '',
            //         email: args.email || '',
            //         password: args.password || ''
            //     };
            //     userData.push(mapUser(newUser));
            //     return newUser;
            // }
            async resolve(parent, args, context) {
                const conn = context?.pool;
                if (!conn) {
                    throw new Error("Database connection not found in context");
                }
                // pre-require: check email format
                if (!args.email?.includes('@')) {
                    throw new Error("Invalid email format");
                }
                try {
                    const [result] = await conn.execute('INSERT INTO users (first_name, last_name, email, password) VALUES (?, ?, ?, ?);', [args.firstName, args.lastName, args.email, args.password]);
                    const InsertId = result.insertId;
                    return {
                        id: InsertId,
                        firstName: args.firstName,
                        lastName: args.lastName,
                        email: args.email,
                        password: args.password
                    };
                }
                catch (error) {
                    console.error("Could not create user");
                    throw new Error("Could not create user");
                }
            }
        },
        UpdateUser: {
            type: UserType,
            args: {
                id: { type: GraphQLInt },
                firstName: { type: GraphQLString },
                lastName: { type: GraphQLString },
                email: { type: GraphQLString },
                password: { type: GraphQLString }
            },
            async resolve(parent, args, context) {
                const conn = context?.pool;
                if (!conn) {
                    throw new Error("Database connection not found in context");
                }
                const fieldToUpdate = [];
                const values = [];
                if (args.firstName !== undefined) {
                    fieldToUpdate.push('first_name = ?');
                    values.push(args.firstName);
                }
                if (args.lastName !== undefined) {
                    fieldToUpdate.push('last_name = ?');
                    values.push(args.lastName);
                }
                if (args.email !== undefined) {
                    if (args.email?.includes('@')) {
                        fieldToUpdate.push('email = ?');
                        values.push(args.email);
                    }
                    else {
                        throw new Error("Invalid email format");
                    }
                }
                if (args.password !== undefined) {
                    fieldToUpdate.push('password = ?');
                    values.push(args.password);
                }
                if (fieldToUpdate.length == 0) {
                    throw new Error("Not found update field to update");
                }
                try {
                    const query = `UPDATE users SET ${fieldToUpdate.join(",")} WHERE id = ?`;
                    values.push(args.id); // Use ! to tell TS id is definitely there if you checked it or (args.id as number)
                    const [rows] = await conn.execute(query, values);
                    const result_update = rows;
                    if (result_update.affectedRows === 0) {
                        throw new Error('not update');
                    }
                    // Fetch and return the updated user (optional, but good practice for GraphQL)
                    const [update_rows] = await conn.query('SELECT * FROM users WHERE id = ? ', [args.id]);
                    return mapUser(update_rows[0]);
                }
                catch (error) {
                    if (error.message === "not update") {
                        throw new Error(`User with id ${args.id} not found.`);
                    }
                    console.error("Could not updated user");
                    throw new Error("Could not updated user");
                }
            }
        },
        deleteUser: {
            type: UserType,
            args: {
                id: { type: GraphQLInt }
            },
            async resolve(parent, args, context) {
                const conn = context?.pool;
                if (!conn) {
                    throw new Error("Database connection not found in context");
                }
                try {
                    // 1. stored delete content for return
                    const [delete_rows] = await conn.query('SELECT * FROM users WHERE id = ? ', [args.id]);
                    // 2. delete content
                    const [rows] = await conn.execute('DELETE FROM users WHERE id = ?', [args.id]);
                    // 3. check for affect rows (if not affect, delete operation is not success)
                    const result = rows;
                    if (result.affectedRows === 0) {
                        throw new Error(`User with id: ${args.id} not found.`);
                    }
                    // 4. return delete content
                    return mapUser(delete_rows[0]);
                }
                catch (error) {
                    console.error("Could not delete user");
                    throw new Error("Could not delete user");
                }
            }
        }
    }
});
//# sourceMappingURL=mutation.js.map