// required library
import express, { type Express, type Request, type Response } from 'express';
import {
    GraphQLSchema
} from "graphql";
// import schema graphql
import { pool } from './database.js';
import {graphqlHTTP} from "express-graphql"
import { RootQuery } from './graphql/query.js';
import { Mutation } from './graphql/mutation.js';

// const userData = require("../../data/MOCK_DATA.csv") as Users[];
// read-only 
// import userData from '../../data/MOCK_DATA.json' with {type: "json"};

// change field name from json
// import userDataRaw from '../../data/MOCK_DATA.json' with {type: "json"};
// const userData: Users[] = userDataRaw.map(u => mapUser(u))

const app: Express = express()

const port: number = 3000

app.use(express.json());

/*
Schema Definition Language(SDL)
! - important (not NULL)
type Users {
    id: int!
    firstName: string!
    lastName: string
    email: string!
    password: string!
}
*/ 


const schema = new GraphQLSchema({
    query: RootQuery,
    mutation: Mutation
});


app.get('/', (req: Request, res: Response) => {
  res.json({
    message: 'Hello Express + TypeScirpt!! & GraphQL'
  })
})

app.post('/show', (req: Request, res:Response) => {
    res.json({
        message: req.body
    })
})

app.use("/graphql", graphqlHTTP((req, res) =>({
    schema,
    graphiql:true,
    context: {
        pool: pool
        // This is where you put things every resolver needs
        // testContext: "data from context"
        // user: (req as any).user, // If you have auth middleware
        // secretKey: "MY_SECRET_KEY" 
    }
})))

app.listen(port, () => console.log(`Application is running on port ${port}`))