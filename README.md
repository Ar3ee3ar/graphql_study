## GraphQL concept
1. query
    - query GetUser {
        getAllUsers {
            id
            firstName
            lastName
            email
            password
        }
    }
    - query GetUser {
        getUser(id: 1004) {
            id
            firstName
            lastName
            email
            password
        }
    }
2. mutation
    - mutation{
        createUser(
            firstName: "a",
            lastName: "b",
            email: "c@c.com",
            password:"nfladkfhaosFB"){
            id,
            firstName,
            lastName,
            email,
            password
        }
    }
    - mutation UpdateUser {
        UpdateUser(id: 1004, email: "b@b.com") {
            id
            firstName
            lastName
            email
            password
        }
    }
    - mutation DeleteUser {
        deleteUser (id: 1004){
            id
            firstName
            lastName
            email
            password
        }
    }


