import { type Users } from "./schema.js";

// named export (use with {export_variable} with exact export named)
export function mapUser(data: any): Users {
    return{
        id: data.id,
        firstName: data.first_name || data.firstName,
        lastName: data.last_name || data.lastName,
        email: data.email,
        password: data.password
    };
}