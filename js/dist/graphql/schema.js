import { GraphQLObjectType, GraphQLSchema, GraphQLInt, GraphQLString, GraphQLList } from "graphql";
const UserType = new GraphQLObjectType({
    name: "User",
    fields: {
        id: { type: GraphQLInt },
        firstName: { type: GraphQLString },
        lastName: { type: GraphQLString },
        email: { type: GraphQLString },
        password: { type: GraphQLString }
    }
});
// export clause (use with {export_variable} can be rename with {export_variable as new_name})
export { UserType };
// default keyword can be used one time for each file (can be used with no braced and can freely renamed e.g. import new_name from ....)
//# sourceMappingURL=schema.js.map