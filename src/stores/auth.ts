import { defineStore } from 'pinia';
export interface User {
    id?: string;
    [key: string]: unknown;
}

export interface AuthState {
    user: User | null;
}

export interface AuthGetters {
    isLoggedIn(state: AuthState): User | null;
}

export interface AuthActions {
    setUser(user: User | null): void;
    clearUser(): void;
}

export interface AuthStore extends AuthState {
    isLoggedIn: User | null;
    setUser(user: User | null): void;
    clearUser(): void;
}

export const useAuthStore = defineStore(
    'auth',
    {
        state: (): AuthState => ({
            user: null,
        }),
        getters: {
            isLoggedIn: (state: AuthState): User | null => state.user,
        },
        actions: {
            setUser(this: AuthStore, user: User | null): void {
                this.user = user;
            },
            clearUser(this: AuthStore): void {
                this.user = null;
            },
        },
    }
);
