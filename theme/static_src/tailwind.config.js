/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

module.exports = {
    content: [
        /**
         * HTML. Paths to Django template files that will contain Tailwind CSS classes.
         */

        /*  Templates within theme app (<tailwind_app_name>/templates), e.g. base.html. */
        '../templates/**/*.html',

        /*
         * Main templates directory of the project (BASE_DIR/templates).
         * Adjust the following line to match your project structure.
         */
        '../../templates/**/*.html',

        /*
         * Templates in other django apps (BASE_DIR/<any_app_name>/templates).
         * Adjust the following line to match your project structure.
         */
        '../../**/templates/**/*.html',

        /* Decoupled frontend pages and scripts */
        '../../frontend/*.html',
        '../../frontend/static/js/**/*.js',

        /**
         * JS: If you use Tailwind CSS in JavaScript, uncomment the following lines and make sure
         * patterns match your project structure.
         */
        /* JS 1: Ignore any JavaScript in node_modules folder. */
        // '!../../**/node_modules',
        /* JS 2: Process all JavaScript files in the project. */
        // '../../**/*.js',

        /**
         * Python: If you use Tailwind CSS classes in Python, uncomment the following line
         * and make sure the pattern below matches your project structure.
         */
        // '../../**/*.py'
    ],
    theme: {
        extend: {
            colors: {
                bg: '#05090D',
                surface: '#0A1018',
                'surface-2': '#0F1720',
                'surface-3': '#141F2A',
                border: '#1C2A38',
                'border-2': '#253648',
                'text-main': '#C8D4DF',
                'text-2': '#637585',
                'text-3': '#374B5C',
                gold: '#C09B2A',
                'gold-dim': '#8A6F1E',
                teal: '#0FC4B3',
                income: '#1DCF72',
                expense: '#E84040',

                // Compatibility aliases
                'bg-primary': '#05090D',
                'bg-secondary': '#0A1018',
                'bg-tertiary': '#141F2A',
                'text-primary': '#C8D4DF',
                'text-secondary': '#637585',
                'text-muted': '#374B5C',
                accent: {
                    500: '#C09B2A',
                    600: '#8A6F1E',
                    700: '#685315',
                },
                success: '#1DCF72',
                error: '#E84040',
                warning: '#C09B2A',
                info: '#0FC4B3',
            },
            fontFamily: {
                sans: ['Inter', 'system-ui', 'sans-serif'],
                display: ['DM Sans', 'sans-serif'],
                mono: ['JetBrains Mono', 'monospace'],
            },
        },
    },
    plugins: [
        /**
         * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
         * for forms. If you don't like it or have own styling for forms,
         * comment the line below to disable '@tailwindcss/forms'.
         */
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
    ],
}
