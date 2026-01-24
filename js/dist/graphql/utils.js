import {} from "./schema.js";
// named export (use with {export_variable} with exact export named)
export function mapUser(data) {
    return {
        id: data.id,
        firstName: data.first_name || data.firstName,
        lastName: data.last_name || data.lastName,
        email: data.email,
        password: data.password
    };
}
//# sourceMappingURL=utils.js.map