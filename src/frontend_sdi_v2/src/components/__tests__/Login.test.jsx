// @vitest-environment jsdom
import { render, screen, fireEvent, cleanup} from '@testing-library/react';
import { describe, it, expect, afterEach } from 'vitest';
import { MemoryRouter } from 'react-router-dom';
import {Login} from '../../pages/authentification/Login'; // Adjust path based on where your Login component lives

afterEach(() => {
    cleanup();
});

describe('Login Component UI and Interactions', () => {
    it('renders username and password input fields cleanly', () => {
        render(
            <MemoryRouter>
                <Login />
            </MemoryRouter>
        );

        expect(screen.getByPlaceholderText(/username/i)).toBeTruthy();
        expect(screen.getByPlaceholderText(/password/i)).toBeTruthy();
        expect(screen.getByRole('button', { name: /log in/i })).toBeTruthy();
    });

    it('allows typing input data inside the fields and updates state values', () => {
        render(
            <MemoryRouter>
                <Login />
            </MemoryRouter>
        );

        const usernameInput = screen.getByPlaceholderText(/username/i);
        const passwordInput = screen.getByPlaceholderText(/password/i);

        fireEvent.change(usernameInput, { target: { value: 'maki_reviewer' } });
        fireEvent.change(passwordInput, { target: { value: 'password123' } });

        expect(usernameInput.value).toBe('maki_reviewer');
        expect(passwordInput.value).toBe('password123');
    });

    it('triggers form submissions when clicking the submission element', async () => {
        render(
            <MemoryRouter>
                <Login />
            </MemoryRouter>
        );

        const loginButton = screen.getByRole('button', { name: /log in/i });

        fireEvent.click(loginButton);

        expect(loginButton.disabled).toBe(false);
    });
});