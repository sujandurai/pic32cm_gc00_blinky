#!/usr/bin/env python3
"""
Build high-quality professional PDF Student Guide using WeasyPrint.
Integrates Microchip and Zephyr full logos, vector SVG diagrams, flowcharts, tables, and structured learning material.
"""

import os
import weasyprint
import shutil

PROJECT_DIR = "/home/sujan/zephyrproject/pic32cm_gc00_blinky"
ASSETS_DIR = "/home/sujan/zephyrproject/pic32cm_gc00_blinky/assets"
OUTPUT_PDF = "/home/sujan/zephyrproject/pic32cm_gc00_blinky/Zephyr_RTOS_PIC32CM_GC00_Student_Guide.pdf"
COPY_ROOT_PDF = "/home/sujan/zephyrproject/Zephyr_RTOS_PIC32CM_GC00_Student_Guide.pdf"

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Zephyr RTOS Student & Beginner's Guide — Microchip PIC32CM GC00 Curiosity Pro</title>
<style>
  @page {{
    size: A4;
    margin: 18mm 15mm 20mm 15mm;
    @top-right {{
      content: "Zephyr RTOS Student Guide";
      font-family: 'DejaVu Sans', Helvetica, Arial, sans-serif;
      font-size: 8pt;
      color: #666;
    }}
    @bottom-left {{
      content: "Microchip PIC32CM GC00 Curiosity Pro (PIC32CM5112GC00100)";
      font-family: 'DejaVu Sans', Helvetica, Arial, sans-serif;
      font-size: 8pt;
      color: #777;
    }}
    @bottom-center {{
      content: "Page " counter(page) " of " counter(pages);
      font-family: 'DejaVu Sans', Helvetica, Arial, sans-serif;
      font-size: 8pt;
      font-weight: bold;
      color: #333;
    }}
    @bottom-right {{
      content: "Microchip Technology Inc.";
      font-family: 'DejaVu Sans', Helvetica, Arial, sans-serif;
      font-size: 8pt;
      color: #C61619;
      font-weight: bold;
    }}
  }}

  @page:first {{
    @top-right {{ content: normal; }}
    @bottom-left {{ content: normal; }}
    @bottom-center {{ content: normal; }}
    @bottom-right {{ content: normal; }}
  }}

  body {{
    font-family: 'DejaVu Sans', 'Liberation Sans', Helvetica, Arial, sans-serif;
    font-size: 9.8pt;
    line-height: 1.55;
    color: #222;
    margin: 0;
    padding: 0;
  }}

  /* Top Banner with Microchip and Zephyr Logos */
  .logo-banner {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 3.5px solid #C61619;
    padding-bottom: 12px;
    margin-bottom: 22px;
  }}
  .logo-microchip {{
    height: 48px;
    object-fit: contain;
  }}
  .logo-zephyr {{
    height: 44px;
    object-fit: contain;
  }}

  .doc-title-box {{
    background: linear-gradient(135deg, #fefdfd 0%, #f4f6f8 100%);
    border-left: 6px solid #C61619;
    padding: 18px 22px;
    border-radius: 4px;
    margin-bottom: 20px;
    border-top: 1px solid #eaecef;
    border-right: 1px solid #eaecef;
    border-bottom: 1px solid #eaecef;
  }}
  h1.main-title {{
    font-size: 21pt;
    color: #C61619;
    margin: 0 0 6px 0;
    font-weight: bold;
    line-height: 1.25;
  }}
  h2.main-subtitle {{
    font-size: 12pt;
    color: #1B4F8A;
    margin: 0 0 12px 0;
    font-weight: 600;
  }}
  .doc-meta {{
    font-size: 8.5pt;
    color: #444;
    display: flex;
    gap: 12px;
  }}
  .doc-meta span {{
    background: #fff;
    padding: 4px 8px;
    border: 1px solid #d0d7de;
    border-radius: 3px;
  }}

  h2.sec-title {{
    color: #1B4F8A;
    font-size: 13.5pt;
    border-bottom: 1.5px solid #1B4F8A;
    padding-bottom: 4px;
    margin-top: 24px;
    margin-bottom: 10px;
    page-break-after: avoid;
  }}
  h3.sub-title {{
    color: #C61619;
    font-size: 11pt;
    margin-top: 16px;
    margin-bottom: 6px;
    page-break-after: avoid;
  }}

  p {{
    margin: 0 0 9px 0;
    text-align: justify;
  }}

  /* Tables */
  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 12px 0;
    font-size: 8.8pt;
    page-break-inside: avoid;
  }}
  th, td {{
    border: 1px solid #d0d7de;
    padding: 7px 9px;
    text-align: left;
    vertical-align: middle;
  }}
  th {{
    background-color: #1B4F8A;
    color: #ffffff;
    font-weight: 600;
  }}
  tr:nth-child(even) {{
    background-color: #f8fafc;
  }}

  /* Callouts & Alert Boxes */
  .callout {{
    padding: 10px 14px;
    border-radius: 4px;
    margin: 12px 0;
    font-size: 9pt;
    page-break-inside: avoid;
  }}
  .callout-info {{
    background-color: #f0f7ff;
    border-left: 5px solid #1B4F8A;
    color: #0b396e;
  }}
  .callout-tip {{
    background-color: #eafaf1;
    border-left: 5px solid #27ae60;
    color: #1e6b37;
  }}
  .callout-warning {{
    background-color: #fff9db;
    border-left: 5px solid #f59f00;
    color: #7a4f01;
  }}
  .callout-title {{
    font-weight: bold;
    margin-bottom: 3px;
    display: block;
    text-transform: uppercase;
    font-size: 8pt;
    letter-spacing: 0.5px;
  }}

  /* Code Blocks */
  pre.code-block {{
    background-color: #1e1e1e;
    color: #dcdcdc;
    font-family: 'Liberation Mono', 'Courier New', monospace;
    font-size: 8.2pt;
    padding: 10px 12px;
    border-radius: 4px;
    line-height: 1.4;
    margin: 10px 0;
    white-space: pre-wrap;
    word-break: break-all;
  }}
  code.inline {{
    background-color: #f1f3f5;
    color: #C61619;
    font-family: 'Liberation Mono', monospace;
    font-size: 8.5pt;
    padding: 1px 4px;
    border-radius: 3px;
    border: 1px solid #e9ecef;
  }}

  /* Diagrams and Images */
  .diagram-container {{
    text-align: center;
    margin: 14px 0;
    page-break-inside: avoid;
  }}
  .diagram-img {{
    max-width: 100%;
    height: auto;
    border: 1px solid #e1e4e8;
    border-radius: 6px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
  }}
  .diagram-caption {{
    font-size: 8pt;
    color: #666;
    margin-top: 5px;
    font-style: italic;
  }}

  .page-break {{
    page-break-after: always;
  }}

  .card-grid {{
    display: flex;
    gap: 10px;
    margin: 12px 0;
    page-break-inside: avoid;
  }}
  .card {{
    flex: 1;
    border: 1px solid #d0d7de;
    border-radius: 5px;
    padding: 10px 12px;
    background: #fafbfc;
  }}
  .card-title {{
    font-weight: bold;
    color: #1B4F8A;
    font-size: 9.5pt;
    margin-bottom: 4px;
  }}

  ul, ol {{
    margin: 0 0 10px 18px;
    padding: 0;
  }}
  li {{
    margin-bottom: 3px;
  }}
</style>
</head>
<body>

  <!-- Top Logo Banner -->
  <div class="logo-banner">
    <img src="{ASSETS_DIR}/microchip_logo.png" class="logo-microchip" alt="Microchip Technology Logo" />
    <img src="{ASSETS_DIR}/zephyr_logo_full.svg" class="logo-zephyr" alt="Zephyr RTOS Logo" />
  </div>

  <!-- Document Header -->
  <div class="doc-title-box">
    <h1 class="main-title">Zephyr RTOS Student & Beginner's Guide</h1>
    <h2 class="main-subtitle">Hands-On Embedded Systems Engineering with Microchip PIC32CM GC00 Curiosity Pro</h2>
    <div class="doc-meta">
      <span><strong>Board:</strong> pic32cm_gc00_cpro</span>
      <span><strong>MCU:</strong> PIC32CM5112GC00100</span>
      <span><strong>Architecture:</strong> ARM Cortex-M23 @ 48 MHz</span>
      <span><strong>Document Version:</strong> 1.0</span>
    </div>
  </div>

  <div class="callout callout-info">
    <span class="callout-title">Curriculum Objective</span>
    This comprehensive laboratory guide introduces university students, electrical engineering candidates, and embedded developers to modern, production-grade real-time systems using <strong>Zephyr RTOS</strong> on the <strong>Microchip PIC32CM GC00 Curiosity Pro</strong> evaluation board.
  </div>

  <!-- Section 1 -->
  <h2 class="sec-title">1. Introduction to Real-Time Operating Systems (RTOS)</h2>
  
  <h3 class="sub-title">1.1 What is an RTOS?</h3>
  <p>
    An <strong>RTOS (Real-Time Operating System)</strong> is an operating system engineered to execute tasks with strict, deterministic timing guarantees. While general-purpose operating systems (Windows, macOS, Linux) optimize for maximum data throughput and user multitasking, an RTOS guarantees that hardware events, sensor readings, and interrupts are serviced within exact microsecond or millisecond boundaries.
  </p>

  <h3 class="sub-title">1.2 Bare-Metal vs. RTOS Paradigm</h3>
  <p>
    Traditional embedded education begins with <strong>Bare-Metal</strong> programming, where firmware executes inside a single <code>while(1)</code> super-loop:
  </p>
  <ul>
    <li><strong>CPU Wastage:</strong> Delays are executed using blocking loops (e.g. <code>for(int i=0; i&lt;100000; i++);</code>), running the core at 100% load and wasting battery energy.</li>
    <li><strong>Inflexible Concurrency:</strong> Adding simultaneous tasks (e.g. blinking an LED while sampling an ADC and receiving UART packets) requires complex interrupt state machines.</li>
    <li><strong>Zero Portability:</strong> Firmware code directly writes vendor-specific registers (e.g., <code>PORTA-&gt;DIRSET.reg = (1 &lt;&lt; 20);</code>). Migrating to a new microcontroller requires rewriting everything from scratch.</li>
  </ul>
  <p>
    In contrast, an <strong>RTOS</strong> provides a <strong>preemptive real-time scheduler</strong>. Each task runs in its own thread with a private stack. When a thread pauses (e.g. <code>k_msleep(350)</code>), the kernel yields the CPU to lower-priority threads or places the MCU into an ultra-low-power idle state until the hardware timer interrupt wakes it.
  </p>

  <h3 class="sub-title">1.3 What is Zephyr RTOS?</h3>
  <p>
    <strong>Zephyr</strong> is an open-source, scalable, highly secure RTOS hosted by the <strong>Linux Foundation</strong> and governed by industry leaders including Microchip, Google, Intel, Nordic Semiconductor, NXP, STMicroelectronics, and Qualcomm. Licensed under the permissive <strong>Apache 2.0</strong> license, Zephyr brings the proven software engineering architecture of the Linux Kernel (Devicetree, Kconfig, modular drivers, POSIX compatibility) down to 32-bit microcontrollers.
  </p>

  <!-- Section 2 -->
  <h2 class="sec-title">2. Why Choose Zephyr? (Purpose & Industry Advantages)</h2>

  <table>
    <thead>
      <tr>
        <th style="width: 25%;">Feature</th>
        <th style="width: 25%;">Bare-Metal (Traditional)</th>
        <th style="width: 25%;">FreeRTOS</th>
        <th style="width: 25%;">Zephyr RTOS</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Hardware Abstraction</strong></td>
        <td>Direct register manipulation</td>
        <td>Vendor HAL dependent</td>
        <td><strong>Devicetree (DTS) Standard</strong></td>
      </tr>
      <tr>
        <td><strong>Build & Configuration</strong></td>
        <td>Manual C header `#define`s</td>
        <td>`FreeRTOSConfig.h`</td>
        <td><strong>Granular Kconfig Engine</strong></td>
      </tr>
      <tr>
        <td><strong>Cross-Vendor Portability</strong></td>
        <td>Zero (Locked to 1 chip)</td>
        <td>Low (Requires vendor glue)</td>
        <td><strong>Universal standardized APIs</strong></td>
      </tr>
      <tr>
        <td><strong>Power Management</strong></td>
        <td>Manual sleep register writes</td>
        <td>Tickless idle (requires glue)</td>
        <td><strong>Native Power Management Subsystem</strong></td>
      </tr>
      <tr>
        <td><strong>Protocol Stacks</strong></td>
        <td>Requires 3rd-party integration</td>
        <td>External ports required</td>
        <td><strong>Built-in BLE, Wi-Fi, CAN, TCP/IP, USB</strong></td>
      </tr>
    </tbody>
  </table>

  <div class="page-break"></div>

  <!-- Section 3: Hardware Overview -->
  <h2 class="sec-title">3. Hardware Architecture: PIC32CM GC00 Curiosity Pro</h2>
  <p>
    The <strong>PIC32CM GC00 Curiosity Pro</strong> evaluation board features the Microchip <strong>PIC32CM5112GC00100</strong>, a 32-bit ARM Cortex-M23 microcontroller equipped with advanced analog and security peripherals.
  </p>

  <div class="diagram-container">
    <img src="{ASSETS_DIR}/board.png" class="diagram-img" style="max-height: 200px;" alt="Microchip PIC32CM GC00 Curiosity Pro Board" />
    <div class="diagram-caption">Figure 1: Microchip PIC32CM GC00 Curiosity Pro Evaluation Kit with Integrated nEDBG Debugger.</div>
  </div>

  <table>
    <thead>
      <tr>
        <th>Specification</th>
        <th>Hardware Value</th>
        <th>Educational Significance</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Processor Core</strong></td>
        <td>ARM Cortex-M23 (ARMv8-M)</td>
        <td>Modern low-power 32-bit RISC architecture with security extensions</td>
      </tr>
      <tr>
        <td><strong>Clock Frequency</strong></td>
        <td>48.0 MHz (FDPLL96M)</td>
        <td>High-speed deterministic instruction execution</td>
      </tr>
      <tr>
        <td><strong>On-Chip Flash</strong></td>
        <td>512 KB</td>
        <td>Stores the Zephyr kernel, RTOS stacks, and user application firmware</td>
      </tr>
      <tr>
        <td><strong>SRAM</strong></td>
        <td>128 KB</td>
        <td>Zero-wait-state memory for thread stacks, heaps, and variables</td>
      </tr>
      <tr>
        <td><strong>Onboard Debugger</strong></td>
        <td>nEDBG (CMSIS-DAP)</td>
        <td>Enables flashing and hardware debugging without external programmer tools</td>
      </tr>
      <tr>
        <td><strong>Primary User LED</strong></td>
        <td><strong>Yellow LED0 on PA20</strong></td>
        <td>Wired in <strong>Active-Low</strong> electrical configuration</td>
      </tr>
    </tbody>
  </table>

  <!-- Active-Low Section -->
  <h3 class="sub-title">3.1 Demystifying Active-Low Electrical Logic</h3>
  <p>
    A critical electrical engineering concept is understanding why the onboard LED on the Curiosity Pro is wired as <strong>Active-Low</strong> rather than Active-High:
  </p>

  <div class="diagram-container">
    <img src="{ASSETS_DIR}/circuit_active_low.svg" class="diagram-img" alt="Active Low vs Active High Circuit Diagram" />
    <div class="diagram-caption">Figure 2: Electrical schematic comparison between traditional Active-High vs. PIC32CM GC00 Active-Low circuitry.</div>
  </div>

  <div class="callout callout-warning">
    <span class="callout-title">Hardware Principle: Current Sinking vs. Sourcing</span>
    Microcontroller I/O pins (internal N-channel MOSFETs) can typically sink more current to Ground (0V) safely than P-channel MOSFETs can source from supply (3.3V). Connecting the LED cathode to pin PA20 ensures maximum brightness and electrical stability.
  </div>

  <p>
    <strong>How Zephyr Handles Active-Low:</strong> In bare-metal code, students must write <code>0</code> to turn the LED ON and <code>1</code> to turn it OFF. In Zephyr, the board's Devicetree defines:
  </p>
  <pre class="code-block">led0: led_0 {{
    gpios = &lt;&amp;porta 20 GPIO_ACTIVE_LOW&gt;;
    label = "LED0";
}};</pre>
  <p>
    Because <code>GPIO_ACTIVE_LOW</code> is declared in Devicetree, Zephyr's <code>gpio_pin_set_dt(&amp;led, 1)</code> activates the LED by driving the pin LOW automatically. You program in logical states: <strong>1 is always ON, 0 is always OFF</strong>!
  </p>

  <div class="page-break"></div>

  <!-- Section 4: System Architecture -->
  <h2 class="sec-title">4. Software Architecture & Timing Specifications</h2>

  <h3 class="sub-title">4.1 Layered Driver Architecture</h3>
  <p>
    Zephyr cleanly isolates application code from physical silicon registers through a multi-tiered driver model:
  </p>

  <div class="diagram-container">
    <img src="{ASSETS_DIR}/architecture_diagram.svg" class="diagram-img" alt="Zephyr Layered Driver Architecture" />
    <div class="diagram-caption">Figure 3: Multi-tier architectural flow from C application to Microchip PORT hardware registers.</div>
  </div>

  <h3 class="sub-title">4.2 Timing Waveform Specification</h3>
  <p>
    The target application generates a deterministic pulsing rhythm: <strong>5 rapid blink cycles</strong> (350 ms ON, 450 ms OFF), followed by an extended <strong>1000 ms quiescent pause</strong>:
  </p>

  <div class="diagram-container">
    <img src="{ASSETS_DIR}/timing_waveform.svg" class="diagram-img" alt="LED Timing Waveform" />
    <div class="diagram-caption">Figure 4: Exact timing diagram showing 5 active pulse cycles (4000 ms) and quiescent pause (1000 ms).</div>
  </div>

  <div class="page-break"></div>

  <h3 class="sub-title">4.3 Program Execution Flowchart</h3>
  <p>
    The firmware executes through the deterministic cyclic state machine depicted below:
  </p>

  <div class="diagram-container">
    <img src="{ASSETS_DIR}/flowchart_diagram.svg" class="diagram-img" alt="Execution Flowchart" />
    <div class="diagram-caption">Figure 5: State machine flowchart showing initialization, 5-burst loop, and 1000 ms rest cycle.</div>
  </div>

  <div class="page-break"></div>

  <!-- Section 5: Development Environment Setup -->
  <h2 class="sec-title">5. Step-by-Step Development Environment Setup Guide</h2>
  <p>
    Follow these instructions to configure your host machine (Linux, Ubuntu 22.04/24.04, or Windows WSL2):
  </p>

  <h3 class="sub-title">Step 1: Install Host Operating System Packages</h3>
  <pre class="code-block">sudo apt update &amp;&amp; sudo apt install -y git cmake ninja-build gperf ccache dfu-util \
  device-tree-compiler wget python3-dev python3-pip python3-setuptools xz-utils make gcc</pre>

  <h3 class="sub-title">Step 2: Initialize Workspace &amp; Install West Meta-Tool</h3>
  <pre class="code-block"># Create workspace and Python virtual environment
mkdir -p ~/zephyrproject &amp;&amp; cd ~/zephyrproject
python3 -m venv .venv
source .venv/bin/activate

# Install West and download Zephyr modules
pip install west
west init -l zephyr
west update
west zephyr-export
pip install -r zephyr/scripts/requirements.txt</pre>

  <h3 class="sub-title">Step 3: Install Zephyr ARM SDK Cross-Compiler</h3>
  <pre class="code-block">wget https://github.com/zephyrproject-rtos/sdk-ng/releases/download/v0.16.8/zephyr-sdk-0.16.8_linux-x86_64.tar.xz
tar xvf zephyr-sdk-0.16.8_linux-x86_64.tar.xz
cd zephyr-sdk-0.16.8 &amp;&amp; ./setup.sh -t arm-zephyr-eabi -h -c</pre>

  <h3 class="sub-title">Step 4: Configure USB udev Rules for Debugger Access</h3>
  <pre class="code-block">sudo cp ~/zephyrproject/zephyr/scripts/udev/rules.d/* /etc/udev/rules.d/
sudo udevadm control --reload-rules &amp;&amp; sudo udevadm trigger</pre>

  <!-- Section 6: Code Walkthrough -->
  <h2 class="sec-title">6. Detailed Code Walkthrough (`src/main.c`)</h2>
  <p>
    Let's examine how each section of the firmware operates:
  </p>

  <h3 class="sub-title">Part 1: Headers &amp; Timing Constants</h3>
  <pre class="code-block">#include &lt;stdio.h&gt;
#include &lt;zephyr/kernel.h&gt;
#include &lt;zephyr/drivers/gpio.h&gt;

#define SLEEP_TIME_MS   1000    /* Quiescent Pause: 1000 ms */
#define ON_TIME         350     /* Active Pulse ON: 350 ms */
#define OFF_TIME        450     /* Inter-pulse OFF: 450 ms */</pre>
  <p>
    <strong>Explanation:</strong> <code>&lt;zephyr/kernel.h&gt;</code> provides kernel sleep services (<code>k_msleep()</code>), and <code>&lt;zephyr/drivers/gpio.h&gt;</code> provides standard GPIO driver APIs. Note that preprocessor macros must not use <code>=</code> assignment operators.
  </p>

  <h3 class="sub-title">Part 2: Devicetree Node Resolution</h3>
  <pre class="code-block">#define LED0_NODE DT_ALIAS(led0)
static const struct gpio_dt_spec led = GPIO_DT_SPEC_GET(LED0_NODE, gpios);</pre>
  <p>
    <strong>Explanation:</strong> <code>DT_ALIAS(led0)</code> queries the board's Devicetree for the alias <code>led0</code>. <code>GPIO_DT_SPEC_GET</code> packages the PORTA driver pointer, pin index 20, and <code>GPIO_ACTIVE_LOW</code> polarity into a static constant structure at compile time.
  </p>

  <div class="page-break"></div>

  <h3 class="sub-title">Part 3: Device Initialization &amp; Readiness</h3>
  <pre class="code-block">int main(void)
{{
    int ret;
    bool led_state;

    if (!gpio_is_ready_dt(&amp;led)) {{
        return 0;
    }}

    ret = gpio_pin_configure_dt(&amp;led, GPIO_OUTPUT_INACTIVE);
    if (ret &lt; 0) {{
        return 0;
    }}</pre>
  <p>
    <strong>Explanation:</strong> <code>gpio_is_ready_dt()</code> verifies that the physical PORT controller initialized without hardware faults. <code>gpio_pin_configure_dt(&amp;led, GPIO_OUTPUT_INACTIVE)</code> sets the pin as an output in the OFF state.
  </p>

  <h3 class="sub-title">Part 4: The Nested 5-Burst Loop &amp; Rest Pause</h3>
  <pre class="code-block">    while (1) {{
        /* Loop 5 times: 350 ms ON, 450 ms OFF */
        for (int i = 0; i &lt; 5; i++) {{
            /* 1. Turn LED ON for 350 ms */
            ret = gpio_pin_set_dt(&amp;led, 1);
            led_state = true;
            printf("Iteration %d/5 - LED state: %s (350 ms ON)\\n", i + 1, "ON");
            k_msleep(ON_TIME);

            /* 2. Turn LED OFF for 450 ms */
            ret = gpio_pin_set_dt(&amp;led, 0);
            led_state = false;
            printf("Iteration %d/5 - LED state: %s (450 ms OFF)\\n", i + 1, "OFF");
            k_msleep(OFF_TIME);
        }}

        /* 3. Quiescent Pause: LED remains OFF for 1000 ms */
        ret = gpio_pin_set_dt(&amp;led, 0);
        printf("Pause - LED state: OFF (1000 ms Pause)\\n\\n");
        k_msleep(SLEEP_TIME_MS);
    }}
    return 0;
}}</pre>
  <p>
    <strong>Explanation:</strong> <code>gpio_pin_set_dt(&amp;led, 1)</code> turns the LED ON. <code>k_msleep(ON_TIME)</code> yields the CPU for 350 ms. After 5 cycles, the LED is turned OFF and sleeps for 1000 ms before repeating.
  </p>

  <!-- Section 7: Build & Flash -->
  <h2 class="sec-title">7. Building, Flashing, and Serial Telemetry</h2>

  <table>
    <thead>
      <tr>
        <th>Action</th>
        <th>Command Line</th>
        <th>Description</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Compile Firmware</strong></td>
        <td><code>west build -b pic32cm_gc00_cpro pic32cm_gc00_blinky -p always</code></td>
        <td>Performs pristine clean build, links Zephyr kernel &amp; outputs ELF/HEX</td>
      </tr>
      <tr>
        <td><strong>Flash Hardware</strong></td>
        <td><code>west flash</code></td>
        <td>Programs firmware directly over USB via the onboard nEDBG debugger</td>
      </tr>
      <tr>
        <td><strong>Monitor Serial Console</strong></td>
        <td><code>picocom -b 115200 /dev/ttyACM0</code></td>
        <td>Connects to the virtual COM port at 115200 baud, 8N1</td>
      </tr>
    </tbody>
  </table>

  <!-- Section 8: Lab Exercises -->
  <h2 class="sec-title">8. Hands-On Student Lab Challenges</h2>

  <div class="card-grid">
    <div class="card">
      <div class="card-title">Lab 1: Morse Code SOS</div>
      <p style="font-size: 8.5pt;">Modify macros to generate international distress signal SOS (3 short pulses of 150ms, 3 long pulses of 450ms, 3 short pulses of 150ms).</p>
    </div>
    <div class="card">
      <div class="card-title">Lab 2: Dual Alternating Beacon</div>
      <p style="font-size: 8.5pt;">Add secondary LED1 (PA18) via <code>DT_ALIAS(led1)</code>. Alternate LED0 and LED1 like an emergency responder beacon.</p>
    </div>
    <div class="card">
      <div class="card-title">Lab 3: Pushbutton Gate</div>
      <p style="font-size: 8.5pt;">Read switch SW0 (PB07) via <code>DT_ALIAS(sw0)</code>. Only run the 5-burst blinking pattern when the button is held pressed.</p>
    </div>
  </div>

  <div style="margin-top: 25px; text-align: center; border-top: 1px solid #ddd; padding-top: 10px; font-size: 8.5pt; color: #777;">
    © 2026 Microchip Technology Inc. &amp; The Zephyr Project. Developed for Embedded Systems University Curriculum.
  </div>

</body>
</html>
"""

temp_html = "/tmp/zephyr_student_guide.html"
with open(temp_html, "w", encoding="utf-8") as f:
    f.write(html_content)

print("HTML generated at:", temp_html)
print("Rendering PDF with WeasyPrint...")
weasyprint.HTML(temp_html).write_pdf(OUTPUT_PDF)
print("PDF successfully generated at:", OUTPUT_PDF)

shutil.copyfile(OUTPUT_PDF, COPY_ROOT_PDF)
print("Copied to workspace root:", COPY_ROOT_PDF)
