import { GraphQLObjectType, GraphQLSchema, GraphQLInt, GraphQLString, GraphQLList } from "graphql";
// const {graphqlHTTP} = require("express-graphql");
// import {graphqlHTTP} from "express-graphql"
import { UserType } from '../graphql/schema.js';
// import {pool} from '../database.js';
import { mapUser } from "./utils.js";
export const RootQuery = new GraphQLObjectType({
    name: "RootQueryType",
    fields: {
        getAllUsers: {
            type: new GraphQLList(UserType), // return Type as list object
            // manage return data
            // resolve: (parent: unknown): Users[] => {
            //     return userData.map(user => mapUser(user));
            // },
            async resolve(parent, args, context) {
                const conn = context?.pool;
                if (!conn) {
                    throw new Error("Database connection not found in context");
                }
                // 1. get data from db
                try {
                    const [rows] = await conn.query('SELECT * FROM users;');
                    return rows.map((row) => mapUser(row));
                    // 2. if error show cause
                }
                catch (error) {
                    console.error("Database error: ", error);
                    throw new Error("Could not fetch users");
                }
            },
            description: "get all users from database"
        },
        getUser: {
            type: UserType, // return as single object
            args: {
                id: { type: GraphQLInt },
            },
            // resolve(parent:unknown, args: {id?: number}): Users | undefined {
            //     const found =  userData.find((user: any) => user.id == args.id);
            //     return found ? mapUser(found) : undefined;
            // },
            async resolve(parent, args, context) {
                const conn = context?.pool;
                if (!conn) {
                    throw new Error("Database connection not found in context");
                }
                try {
                    // console.log(args.id);
                    // 1. query user based on id
                    const [rows] = await conn.query('SELECT * FROM users WHERE id = ? ', [args.id]);
                    if (rows.length === 0) {
                        throw new Error(`Could not fetch user with id: ${args.id}`);
                    }
                    return rows ? mapUser(rows[0]) : null; // use single object to return (if result is null, it doesn't know how to handle an array where it expects one object. )
                }
                // 2. if error show cause message
                catch (error) {
                    console.error("Database error: ", error);
                    throw new Error("Could not fetch users: " + args.id);
                }
            },
            description: "get user by id"
        }
    }
});
//# sourceMappingURL=query.js.map