import { GraphQLObjectType } from "graphql";
declare const UserType: GraphQLObjectType<any, any>;
interface Users {
    id: number;
    firstName: string;
    lastName: string | '';
    email: string;
    password: string;
}
export { UserType, type Users };
//# sourceMappingURL=schema.d.ts.map