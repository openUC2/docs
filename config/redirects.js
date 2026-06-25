const redirectsMinimal = [
	{
		from: "/docs/Toolboxes/DiscoveryCore/ENGLISH/",
		to: "/usage/disc/corebox/en/",
	},
	{
		from: "/docs/Toolboxes/DiscoveryCore/ENGLISH/coreBOXen",
		to: "/usage/disc/corebox/en/core_intro",
	},
	{
		from: "/docs/Toolboxes/DiscoveryCore/ITALIAN/coreBOXit",
		to: "/usage/disc/corebox/it/core_intro",
	},
	{
		from: "/docs/Toolboxes/ElectronicsBox/",
		to: "/usage/disc/electronics-addon/",
	},
	{
		from: "/docs/Toolboxes/ElectronicsBox/automation_intro",
		to: "/usage/disc/electronics-addon/automation_intro",
	},
	{
		from: "/docs/Toolboxes/InfinityBox/",
		to: "/usage/disc/infinity-addon/",
	},
	{
		from: "/docs/Toolboxes/InfinityBox/ABBE",
		to: "/usage/disc/infinity-addon/ABBE",
	},
	{
		from: "/docs/Toolboxes/InfinityBox/DPCmicroscopy",
		to: "/usage/disc/infinity-addon/DPCmicroscopy",
	},
	{
		from: "/docs/Toolboxes/DiscoveryFluorescence/",
		to: "/usage/disc/fluorescence-addon/",
	},
	{
		from: "/docs/Toolboxes/DiscoveryFluorescence/LED_Fluoresence_microscope_V1",
		to: "/usage/disc/fluorescence-addon/LED_Fluoresence_microscope_V1",
	},
	{
		from: "/docs/Toolboxes/DiscoveryFluorescence/LASER_Fluoresence_microscope",
		to: "/usage/disc/fluorescence-addon/LASER_Fluoresence_microscope",
	},
	{
		from: "/docs/Toolboxes/GalvoBox/",
		to: "/usage/disc/galvo-addon/",
	},
	{
		from: "/docs/Toolboxes/GalvoBox/GalvoIntro",
		to: "/usage/disc/galvo-addon/reference",
	},
	{
		from: "/docs/Toolboxes/GalvoBox/LaserScanner",
		to: "/usage/disc/galvo-addon/LaserScanner",
	},
	{
		from: "/docs/Toolboxes/GalvoBox/Profiling",
		to: "/usage/disc/galvo-addon/Profiling",
	},
	{
		from: "/docs/Toolboxes/HoloBox/",
		to: "/usage/disc/holobox/",
	},
	{
		from: "/docs/Toolboxes/LightsheetBox/",
		to: "/usage/disc/lightsheet-addon/",
	},
	{
		from: "/docs/Toolboxes/LightsheetBox/Light_sheet_Fluoresence_microscope",
		to: "/usage/disc/lightsheet-addon/Light_sheet_Fluoresence_microscope",
	},
	{
		from: "/docs/Toolboxes/LightsheetBox/LightSheet%20Sample",
		to: "/usage/disc/lightsheet-addon/LightSheet%20Sample",
	},
	{
		from: "/docs/Toolboxes/LightsheetBox/LightsheetCalibration",
		to: "/usage/disc/lightsheet-addon/LightsheetCalibration",
	},
	{
		from: [
			"/docs/Toolboxes/FourierOptics/",
			"/docs/Toolboxes/FourierOptics/MicroscopyCore",
			"/docs/Toolboxes/FourierOptics/CBoxAligmentFinite",
			"/docs/Toolboxes/FourierOptics/CBoxAligmentInfinte",
		],
		to: "/dev/examples/",
	},
	{
		from: "/docs/Investigator/FRAME/Electronics/FRAMEElectronics",
		to: "/dev/hw/electronics/frame/",
	},
	{
		from: "/docs/Investigator/FRAME/",
		to: "/usage/pro/frame",
	},
	{
		from: [
			"/docs/Investigator/FRAME/Cover_Page",
			"/docs/Investigator/FRAME/Safety_and_Compliance",
			"/docs/Investigator/FRAME/Technical_Specifications",
			"/docs/Investigator/FRAME/Appendix",
		],
		to: "/usage/pro/frame/reference/",
	},
	{
		from: "/docs/Investigator/FRAME/Introduction_and_Overview",
		to: "/usage/pro/frame/explanations",
	},
	{
		from: "/docs/Investigator/FRAME/Installation_and_Setup",
		to: "/usage/pro/frame/guides/day-1/",
	},
	{
		from: "/docs/Investigator/FRAME/Operation_Manual",
		to: "/usage/pro/frame/guides/day-2/",
	},
	{
		from: "/docs/Investigator/FRAME/Maintenance_and_Troubleshooting",
		to: "/usage/pro/frame/guides/day-n/",
	},
	{
		from: "/docs/Investigator/miniFRAME/",
		to: "/usage/pro/miniframe/",
	},
	{
		from: "/docs/Investigator/miniFRAME/miniFRAME_DPC",
		to: "/usage/pro/miniframe/miniFRAME_DPC",
	},
	{
		from: "/docs/Investigator/miniFRAME/miniFRAME_Software",
		to: "/usage/pro/miniframe/miniFRAME_Software",
	},
	{
		from: "/docs/Investigator/Addons/FocusLock",
		to: "/usage/pro/frame/addons/focus-lock/",
	},
	{
		from: [
			"/docs/Investigator/STORM/",
			"/docs/Investigator/STORM/Main",
			"/docs/Investigator/STORM/Illumination",
			"/docs/Investigator/STORM/Stability",
			"/docs/Investigator/STORM/Software",
			"/docs/Investigator/STORM/Electronics",
			"/docs/Investigator/STORM/Results",
		],
		to: "/dev/examples/#proof-of-concept",
	},
	{
		from: "/docs/Investigator/New_OSSIM/",
		to: "/dev/examples/os-sim/",
	},
	{
		from: "/docs/Investigator/New_OSSIM/OS-SIM",
		to: "/dev/examples/os-sim/tutorial",
	},
	{
		from: "/docs/ImSwitch/Quickstart",
		to: "/dev/sw/imswitch/Quickstart",
	},
];

const redirectsQBox = [
	{
		from: "/docs/Toolboxes/QuantumBox/",
		to: "/usage/disc/qbox/",
	},
	{
		from: "/docs/Toolboxes/QuantumBox/MichelsonInterferometer/MichelsonInterferometer",
		to: "/usage/disc/qbox/MichelsonInterferometer/",
	},
	{
		from: "/docs/Toolboxes/QuantumBox/MachZehnderInterferometer/MachZenderInterferometer",
		to: "/usage/disc/qbox/MachZehnderInterferometer/mach-zehnder_interferometer",
	},
	{
		from: "/docs/Toolboxes/QuantumBox/MachZehnderInterferometer/OffAxisHolography",
		to: "/usage/disc/qbox/MachZehnderInterferometer/off_axis_holography",
	},
	{
		from: "/docs/Toolboxes/QuantumBox/DiscoveryPolarization/",
		to: "/usage/disc/qbox/DiscoveryPolarization/",
	},
	{
		from: "/docs/Toolboxes/QuantumBox/DiscoveryPolarization/APP_POL_Crossed_Polarizers/",
		to: "/usage/disc/qbox/DiscoveryPolarization/APP_POL_Crossed_Polarizers/",
	},
	{
		from: "/docs/Toolboxes/QuantumBox/DiscoveryPolarization/APP_POL_Stress_Birefringence/",
		to: "/usage/disc/qbox/DiscoveryPolarization/APP_POL_Stress_Birefringence/",
	},
	{
		from: "/docs/Toolboxes/QuantumBox/DiscoveryPolarization/APP_POL_Three_Polarizers/",
		to: "/usage/disc/qbox/DiscoveryPolarization/APP_POL_Three_Polarizers/",
	},
	{
		from: "/docs/Toolboxes/QuantumBox/ODMR/ENG/odmr_intro_eng",
		to: "/usage/disc/qbox/ODMR/en/odmr_intro_eng",
	},
	{
		from: "/docs/Toolboxes/QuantumBox/ODMR/ENG/odmr_experiment_eng",
		to: "/usage/disc/qbox/ODMR/en/odmr_experiment_eng",
	},
	{
		from: "/docs/Toolboxes/QuantumBox/ODMR/GER/odmr_intro_ger",
		to: "/usage/disc/qbox/ODMR/de/odmr_intro_ger",
	},
	{
		from: "/docs/Toolboxes/QuantumBox/ODMR/GER/odmr_experiment_ger",
		to: "/usage/disc/qbox/ODMR/de/odmr_experiment_ger",
	},
];

const redirectsXiaoMicroscope = [
	{
		from: "/docs/Toolboxes/SeeedMicroscope/",
		to: "/usage/disc/xiao-microscope/",
	},
	{
		from: "/docs/Toolboxes/SeeedMicroscope/04_1_seeedmicroscope",
		to: "/usage/disc/xiao-microscope/04_1_seeedmicroscope",
	},
	{
		from: "/docs/Toolboxes/SeeedMicroscope/04_2_seeedmicroscopepcb",
		to: "/usage/disc/xiao-microscope/04_2_seeedmicroscopepcb",
	},
	{
		from: "/docs/Toolboxes/SeeedMicroscope/04_3_seeedmicroscoperepair",
		to: "/usage/disc/xiao-microscope/04_3_seeedmicroscoperepair",
	},
	{
		from: "/docs/Toolboxes/SeeedMicroscope/04_4_seeedmicroscopeapp",
		to: "/usage/disc/xiao-microscope/04_4_seeedmicroscopeapp",
	},
];

const redirectsWorkshops = [
	{
		from: "/docs/WORKSHOPS/",
		to: "/workshops/",
	},
	{
		from: "/docs/WORKSHOPS/Opticsintro",
		to: "/workshops/Opticsintro",
	},
	{
		from: "/docs/WORKSHOPS/DigitalMicroscopy",
		to: "/workshops/DigitalMicroscopy",
	},
];

const redirectsArchived = [
	{
		from: "/docs/Toolboxes/DiscoveryCore/ARABIAN/uc2miniboxAR",
		to: "/archive/minibox/ar/uc2miniboxAR",
	},
	{
		from: "/docs/Toolboxes/DiscoveryCore/ENGLISH/uc2miniboxEN",
		to: "/archive/minibox/en/uc2miniboxEN",
	},
	{
		from: "/docs/Toolboxes/DiscoveryCore/FRENCH/uc2miniboxFR",
		to: "/archive/minibox/fr/uc2miniboxFR",
	},
	{
		from: "/docs/Toolboxes/DiscoveryCore/GERMAN/uc2miniboxDE",
		to: "/archive/minibox/de/uc2miniboxDE",
	},
	{
		from: "/docs/Toolboxes/DiscoveryCore/ITALIAN/uc2miniboxIT",
		to: "/archive/minibox/it/uc2miniboxIT",
	},
	{
		from: "/docs/Toolboxes/DiscoveryCore/SPANISH/uc2miniboxES",
		to: "/archive/minibox/es/uc2miniboxES",
	},
];

const makeRedirects = (variant) => {
	switch (variant) {
		case "minimal":
			return redirectsMinimal;
		case "full":
			return [
				...redirectsMinimal,
				...redirectsQBox,
				...redirectsXiaoMicroscope,
				...redirectsWorkshops,
				...redirectsArchived,
			];
	}
};

module.exports = makeRedirects;
