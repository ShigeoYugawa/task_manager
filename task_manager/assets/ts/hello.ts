// assets/ts/hello.ts

class Person {
    name: string;
    constructor(name: string) {
        this.name = name;
    }
    greet() {
        return `Hello, ${this.name}!`;
    }
}

class Employee extends Person {
    jobTitle: string;
    constructor(name: string, jobTitle: string) {
        super(name);
        this.jobTitle = jobTitle;
    }
    greet() {
        return `Hello, ${this.name}! You are a ${this.jobTitle}.`;
    }
}

// 使用例
const alice = new Person("Alice");
console.log(alice.greet());

const bob = new Employee("Bob", "Engineer");
console.log(bob.greet());
