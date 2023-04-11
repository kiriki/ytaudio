interface UserData {
  id: number
  username: string
  email: string
}

export default class User {
  id: number
  username: string
  email: string

  constructor (data: UserData) {
    this.id = data.id
    this.username = data.username
    this.email = data.email

    Object.assign(this, data)
  }
}
