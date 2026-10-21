#!/usr/bin/env python3
"""
Generate vector SVG diagrams for the Zephyr RTOS PIC32CM GC00 Student Guide.
"""
import os

ASSETS_DIR = "/home/sujan/zephyrproject/pic32cm_gc00_blinky/assets"
os.makedirs(ASSETS_DIR, exist_ok=True)

# 1. Timing Waveform SVG
timing_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 950 240" width="100%" height="240">
  <defs>
    <style>
      .label { font-family: 'DejaVu Sans', Helvetica, Arial, sans-serif; font-size: 12px; fill: #333; }
      .bold { font-weight: bold; }
      .time-label { font-family: 'DejaVu Sans', Helvetica, Arial, sans-serif; font-size: 11px; fill: #666; text-anchor: middle; }
      .grid { stroke: #e0e0e0; stroke-dasharray: 4,4; stroke-width: 1; }
      .wave { stroke: #d12420; stroke-width: 3.5; fill: none; stroke-linejoin: round; }
      .axis { stroke: #888; stroke-width: 1.5; }
      .fill-on { fill: rgba(209, 36, 32, 0.12); }
      .bracket { stroke: #444; stroke-width: 1.5; fill: none; }
      .ann-text { font-family: 'DejaVu Sans', Helvetica, Arial, sans-serif; font-size: 11px; fill: #1b4f8a; font-weight: bold; text-anchor: middle; }
    </style>
  </defs>

  <!-- Background Card -->
  <rect x="5" y="5" width="940" height="230" rx="8" fill="#fafafa" stroke="#dcdcdc" stroke-width="1.5"/>

  <!-- Left Header -->
  <text x="30" y="45" class="label bold" font-size="14" fill="#1b4f8a">LED Output Timing Waveform (PA20 Active State)</text>
  <text x="30" y="90" class="label bold" fill="#d12420">LED ON</text>
  <text x="30" y="150" class="label bold" fill="#777">LED OFF</text>

  <!-- Level Guidelines -->
  <line x1="100" y1="85" x2="920" y2="85" class="grid"/>
  <line x1="100" y1="145" x2="920" y2="145" class="grid"/>

  <!-- Waveform: 5 pulses of 350ms ON (w=42) and 450ms OFF (w=54), then 1000ms OFF (w=120) -->
  <!-- Burst 1 -->
  <rect x="110" y="85" width="45" height="60" class="fill-on"/>
  <!-- Burst 2 -->
  <rect x="215" y="85" width="45" height="60" class="fill-on"/>
  <!-- Burst 3 -->
  <rect x="320" y="85" width="45" height="60" class="fill-on"/>
  <!-- Burst 4 -->
  <rect x="425" y="85" width="45" height="60" class="fill-on"/>
  <!-- Burst 5 -->
  <rect x="530" y="85" width="45" height="60" class="fill-on"/>

  <!-- Continuous Wave Line -->
  <path d="M 100 145 
           L 110 145 L 110 85 L 155 85 L 155 145 
           L 215 145 L 215 85 L 260 85 L 260 145 
           L 320 145 L 320 85 L 365 85 L 365 145 
           L 425 145 L 425 85 L 470 85 L 470 145 
           L 530 145 L 530 85 L 575 85 L 575 145 
           L 890 145" class="wave"/>

  <!-- Pulse 1 timing annotations -->
  <line x1="110" y1="75" x2="155" y2="75" class="bracket"/>
  <text x="132" y="70" class="time-label bold" fill="#d12420">350ms</text>

  <line x1="155" y1="75" x2="215" y2="75" class="bracket"/>
  <text x="185" y="70" class="time-label">450ms</text>

  <!-- Cycle labels -->
  <text x="132" y="165" class="time-label bold">Cycle 1</text>
  <text x="237" y="165" class="time-label bold">Cycle 2</text>
  <text x="342" y="165" class="time-label bold">Cycle 3</text>
  <text x="447" y="165" class="time-label bold">Cycle 4</text>
  <text x="552" y="165" class="time-label bold">Cycle 5</text>

  <!-- Total 5-Burst Bracket -->
  <path d="M 110 185 L 110 195 L 342 195 L 342 205 L 342 195 L 575 195 L 575 185" class="bracket"/>
  <text x="342" y="220" class="ann-text">Active Burst Phase: 5 Iterations (4000 ms total)</text>

  <!-- 1000ms Pause Annotation -->
  <path d="M 575 185 L 575 195 L 732 195 L 732 205 L 732 195 L 890 195 L 890 185" class="bracket"/>
  <text x="732" y="220" class="ann-text" fill="#d12420">Quiescent Pause: 1000 ms (LED OFF)</text>
</svg>"""

with open(os.path.join(ASSETS_DIR, "timing_waveform.svg"), "w") as f:
    f.write(timing_svg)

# 2. Active-Low vs Active-High Circuit SVG
circuit_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 850 250" width="100%" height="250">
  <defs>
    <style>
      .title { font-family: 'DejaVu Sans', sans-serif; font-size: 13px; font-weight: bold; fill: #1b4f8a; }
      .lbl { font-family: 'DejaVu Sans', sans-serif; font-size: 11px; fill: #333; }
      .code-lbl { font-family: monospace; font-size: 11px; font-weight: bold; fill: #d12420; }
      .wire { stroke: #222; stroke-width: 2; fill: none; }
      .pin { fill: #f0f4f8; stroke: #1b4f8a; stroke-width: 2; rx: 4; }
      .resistor { fill: #fff; stroke: #333; stroke-width: 2; }
      .led-body { fill: #ffe066; stroke: #e67700; stroke-width: 1.5; }
      .badge-ok { fill: #2b8a3e; font-family: sans-serif; font-size: 11px; font-weight: bold; fill: #fff; }
    </style>
  </defs>

  <!-- Box 1: Active-High -->
  <rect x="15" y="10" width="395" height="230" rx="8" fill="#fdfdfd" stroke="#ccc" stroke-width="1.5"/>
  <text x="30" y="35" class="title">Traditional Active-High Circuit</text>

  <!-- MCU Pin Box -->
  <rect x="35" y="65" width="80" height="70" class="pin"/>
  <text x="75" y="95" class="lbl" text-anchor="middle" font-weight="bold">MCU Pin</text>
  <text x="75" y="115" class="lbl" text-anchor="middle" fill="#666">Push-Pull</text>

  <!-- Wires & Components -->
  <line x1="115" y1="100" x2="160" y2="100" class="wire"/>
  
  <!-- LED Triangle -->
  <polygon points="160,85 195,100 160,115" class="led-body"/>
  <line x1="195" y1="85" x2="195" y2="115" class="wire"/>
  <text x="177" y="75" class="lbl" text-anchor="middle">LED</text>

  <!-- Resistor -->
  <line x1="195" y1="100" x2="230" y2="100" class="wire"/>
  <rect x="230" y="90" width="50" height="20" class="resistor"/>
  <text x="255" y="104" class="lbl" text-anchor="middle">330 Ω</text>
  <line x1="280" y1="100" x2="330" y2="100" class="wire"/>

  <!-- GND Symbol -->
  <line x1="330" y1="100" x2="330" y2="120" class="wire"/>
  <line x1="315" y1="120" x2="345" y2="120" class="wire" stroke-width="2.5"/>
  <line x1="320" y1="126" x2="340" y2="126" class="wire" stroke-width="2"/>
  <line x1="325" y1="132" x2="335" y2="132" class="wire" stroke-width="1.5"/>
  <text x="330" y="148" class="lbl" text-anchor="middle">GND (0V)</text>

  <rect x="35" y="165" width="355" height="55" rx="5" fill="#f8f9fa" stroke="#e9ecef"/>
  <text x="45" y="185" class="lbl">• Logic HIGH (3.3V) = Current flows = <tspan font-weight="bold" fill="#2b8a3e">LED ON</tspan></text>
  <text x="45" y="205" class="lbl">• Logic LOW (0.0V) = No current = <tspan font-weight="bold" fill="#c92a2a">LED OFF</tspan></text>

  <!-- Box 2: Active-Low (Curiosity Pro) -->
  <rect x="435" y="10" width="395" height="230" rx="8" fill="#fff9db" stroke="#f59f00" stroke-width="2"/>
  <text x="450" y="35" class="title" fill="#d9480f">PIC32CM GC00 Circuit: Active-Low (LED0 on PA20)</text>

  <!-- VCC 3.3V Line -->
  <text x="475" y="80" class="lbl" text-anchor="middle" font-weight="bold" fill="#d12420">VCC (+3.3V)</text>
  <line x1="475" y1="85" x2="475" y2="100" class="wire"/>
  <circle cx="475" cy="85" r="3" fill="#d12420"/>

  <line x1="475" y1="100" x2="520" y2="100" class="wire"/>
  <!-- Resistor -->
  <rect x="520" y="90" width="50" height="20" class="resistor"/>
  <text x="545" y="104" class="lbl" text-anchor="middle">330 Ω</text>
  <line x1="570" y1="100" x2="610" y2="100" class="wire"/>

  <!-- LED Triangle pointing toward pin -->
  <polygon points="610,85 645,100 610,115" class="led-body"/>
  <line x1="645" y1="85" x2="645" y2="115" class="wire"/>
  <text x="627" y="75" class="lbl" text-anchor="middle">LED0</text>

  <!-- MCU Pin Box PA20 -->
  <line x1="645" y1="100" x2="685" y2="100" class="wire"/>
  <rect x="685" y="65" width="115" height="70" class="pin" fill="#e7f5ff" stroke="#1b4f8a"/>
  <text x="742" y="93" class="lbl" text-anchor="middle" font-weight="bold">Pin PA20</text>
  <text x="742" y="112" class="lbl" text-anchor="middle" fill="#d12420" font-weight="bold">Current Sink</text>

  <rect x="455" y="165" width="355" height="55" rx="5" fill="#fff" stroke="#ffec99"/>
  <text x="465" y="185" class="lbl">• MCU drives 0V (LOW): Sinks current = <tspan font-weight="bold" fill="#2b8a3e">LED ON</tspan></text>
  <text x="465" y="205" class="lbl">• Zephyr handles this: <tspan class="code-lbl">gpio_pin_set_dt(&amp;led, 1) -&gt; ON</tspan></text>
</svg>"""

with open(os.path.join(ASSETS_DIR, "circuit_active_low.svg"), "w") as f:
    f.write(circuit_svg)

# 3. System Architecture SVG
arch_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 850 360" width="100%" height="360">
  <defs>
    <style>
      .hdr { font-family: 'DejaVu Sans', sans-serif; font-size: 13px; font-weight: bold; }
      .sub { font-family: 'DejaVu Sans', sans-serif; font-size: 11px; fill: #444; }
      .box { rx: 6; stroke-width: 1.8; }
      .arrow { stroke: #1b4f8a; stroke-width: 2.2; fill: none; marker-end: url(#arrowhead); }
    </style>
    <marker id="arrowhead" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
      <polygon points="0 0, 8 3, 0 6" fill="#1b4f8a" />
    </marker>
  </defs>

  <rect x="5" y="5" width="840" height="350" rx="8" fill="#fdfdfd" stroke="#dcdcdc" stroke-width="1.5"/>

  <!-- Layer 1: Application -->
  <rect x="30" y="25" width="790" height="60" class="box" fill="#e8f4fd" stroke="#1b4f8a"/>
  <text x="50" y="50" class="hdr" fill="#1b4f8a">1. Application Layer (src/main.c)</text>
  <text x="50" y="70" class="sub">Portable C logic: k_msleep(ON_TIME), gpio_pin_set_dt(&amp;led, 1), printf() serial telemetry</text>

  <!-- Connectors -->
  <line x1="220" y1="85" x2="220" y2="115" class="arrow"/>
  <line x1="620" y1="85" x2="620" y2="115" class="arrow"/>

  <!-- Layer 2: Zephyr OS Subsystems -->
  <rect x="30" y="115" width="380" height="75" class="box" fill="#f3f0ff" stroke="#6741d9"/>
  <text x="50" y="140" class="hdr" fill="#6741d9">2A. Zephyr Devicetree Subsystem</text>
  <text x="50" y="160" class="sub">Resolves DT_ALIAS(led0) at compile-time</text>
  <text x="50" y="177" class="sub">Extracts pin PA20 &amp; GPIO_ACTIVE_LOW flags</text>

  <rect x="440" y="115" width="380" height="75" class="box" fill="#e6fcf5" stroke="#0ca678"/>
  <text x="460" y="140" class="hdr" fill="#0ca678">2B. Zephyr Kernel &amp; GPIO Driver API</text>
  <text x="460" y="160" class="sub">Tickless idle scheduler, k_msleep() yield</text>
  <text x="460" y="177" class="sub">Universal GPIO interface: gpio_pin_configure_dt()</text>

  <!-- Connectors -->
  <line x1="220" y1="190" x2="425" y2="220" class="arrow"/>
  <line x1="630" y1="190" x2="425" y2="220" class="arrow"/>

  <!-- Layer 3: Hardware Drivers -->
  <rect x="30" y="220" width="790" height="55" class="box" fill="#fff4e6" stroke="#f76707"/>
  <text x="50" y="243" class="hdr" fill="#d9480f">3. Microchip Low-Level HAL &amp; Drivers (gpio_mchp_port_g1.c)</text>
  <text x="50" y="262" class="sub">Translates generic Zephyr calls into physical PORT register writes (PORTA-&gt;OUTTGL, DIRSET)</text>

  <!-- Connector -->
  <line x1="425" y1="275" x2="425" y2="295" class="arrow"/>

  <!-- Layer 4: Physical Silicon & Hardware -->
  <rect x="30" y="295" width="790" height="50" class="box" fill="#ffe3e3" stroke="#e03131"/>
  <text x="50" y="318" class="hdr" fill="#c92a2a">4. Microchip PIC32CM GC00 Silicon &amp; Curiosity Pro Board</text>
  <text x="50" y="335" class="sub">ARM Cortex-M23 @ 48 MHz | Pin PA20 drives Yellow LED0 (Active-Low) | UART on PA04</text>
</svg>"""

with open(os.path.join(ASSETS_DIR, "architecture_diagram.svg"), "w") as f:
    f.write(arch_svg)

print("SVG Diagrams successfully generated in:", ASSETS_DIR)
