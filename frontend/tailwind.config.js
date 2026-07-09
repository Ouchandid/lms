import frappeUIPreset from 'frappe-ui/tailwind'

export default {
	presets: [frappeUIPreset],
	content: [
		'./index.html',
		'./src/**/*.{vue,js,ts,jsx,tsx}',
		'./node_modules/frappe-ui/src/**/*.{vue,js,ts,jsx,tsx}',
		'../node_modules/frappe-ui/src/**/*.{vue,js,ts,jsx,tsx}',
		'./node_modules/frappe-ui/frappe/**/*.{vue,js,ts,jsx,tsx}',
		'../node_modules/frappe-ui/frappe/**/*.{vue,js,ts,jsx,tsx}',
	],
	theme: {
		extend: {
			strokeWidth: {
				1.5: '1.5',
			},
			screens: {
				'2xl': '1600px',
				'3xl': '1920px',
			},
			// Islamic academy palette — retints any component using the raw
			// gray/green Tailwind scale directly instead of frappe-ui's
			// semantic surface-*/text-ink-* CSS-variable tokens.
			colors: {
				gray: {
					50: '#F7F1E3',
					100: '#FBF6EC',
					200: '#F2E6C6',
					300: '#E4DCC4',
					400: '#D8CDA9',
					500: '#8A968F',
					600: '#5A6B64',
					700: '#17322B',
					800: '#0A4D39',
					900: '#0B2137',
					950: '#0A1929',
				},
				green: {
					50: '#E4F0EA',
					100: '#E4F0EA',
					200: '#BFE0D0',
					300: '#8FC9AC',
					400: '#4E9C7D',
					500: '#0F6B4F',
					600: '#0A4D39',
					700: '#0A4D39',
					800: '#17322B',
					900: '#0B2137',
				},
			},
		},
	},
	plugins: [],
}
