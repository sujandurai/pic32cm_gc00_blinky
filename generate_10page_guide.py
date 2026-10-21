#!/usr/bin/env python3
"""
Generate an exact 10-page, beautifully styled Zephyr RTOS Student Guide for PIC32CM GC00 Curiosity Pro.
Theme colors matched to user uploaded platform slide:
- Primary Deep Navy Blue: #003B71
- Accent Vibrant Cyan: #00A3E0
- Soft Background Cyan: #EBF7FD
- Clean modern cards, pill badges (01, 02), wave vector accents, and dual Microchip + Zephyr logos.
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
<title>Zephyr RTOS Student Guide — Microchip PIC32CM GC00 Curiosity Pro</title>
<style>
  @page {{
    size: A4;
    margin: 14mm 15mm 16mm 15mm;
    @top-left {{
      content: "Microchip Technology | Zephyr RTOS Student Guide";
      font-family: 'DejaVu Sans', Helvetica, Arial, sans-serif;
      font-size: 7.8pt;
      color: #003B71;
      font-weight: bold;
    }}
    @top-right {{
      content: "PIC32CM GC00 Curiosity Pro";
      font-family: 'DejaVu Sans', Helvetica, Arial, sans-serif;
      font-size: 7.8pt;
      color: #00A3E0;
      font-weight: bold;
    }}
    @bottom-left {{
      content: "PIC32CM5112GC00100 (ARM Cortex-M23)";
      font-family: 'DejaVu Sans', Helvetica, Arial, sans-serif;
      font-size: 7.8pt;
      color: #555;
    }}
    @bottom-center {{
      content: "Page " counter(page) " of " counter(pages);
      font-family: 'DejaVu Sans', Helvetica, Arial, sans-serif;
      font-size: 8pt;
      font-weight: bold;
      color: #003B71;
    }}
    @bottom-right {{
      content: "Lab Curriculum Manual";
      font-family: 'DejaVu Sans', Helvetica, Arial, sans-serif;
      font-size: 7.8pt;
      color: #00A3E0;
      font-weight: bold;
    }}
  }}

  body {{
    font-family: 'DejaVu Sans', 'Liberation Sans', Helvetica, Arial, sans-serif;
    font-size: 9.3pt;
    line-height: 1.48;
    color: #2D3748;
    margin: 0;
    padding: 0;
  }}

  .page-box {{
    page-break-after: always;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    position: relative;
    box-sizing: border-box;
  }}
  .page-box:last-child {{
    page-break-after: avoid;
  }}

  /* Top Dual Logo Header */
  .logo-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 2.5px solid #00A3E0;
    padding-bottom: 8px;
    margin-bottom: 12px;
  }}
  .logo-img {{
    height: 38px;
    object-fit: contain;
  }}

  /* Title Card with Wave Decor */
  .title-card {{
    background: linear-gradient(135deg, #EBF7FD 0%, #F5FBFE 100%);
    border-left: 6px solid #003B71;
    border-top: 1px solid #D0EBF8;
    border-right: 1px solid #D0EBF8;
    border-bottom: 1px solid #D0EBF8;
    border-radius: 4px;
    padding: 12px 18px;
    margin-bottom: 14px;
  }}
  h1.page-title {{
    font-size: 17pt;
    color: #003B71;
    margin: 0 0 4px 0;
    font-weight: bold;
    line-height: 1.25;
  }}
  .page-subtitle {{
    font-size: 10pt;
    color: #00A3E0;
    font-weight: 600;
    margin: 0 0 6px 0;
  }}

  h2.sec-heading {{
    color: #003B71;
    font-size: 12pt;
    border-bottom: 1.5px solid #00A3E0;
    padding-bottom: 3px;
    margin-top: 10px;
    margin-bottom: 8px;
  }}
  h3.sub-heading {{
    color: #003B71;
    font-size: 10.2pt;
    margin-top: 10px;
    margin-bottom: 4px;
  }}

  /* Badge Pills matching uploaded image (01, 02) */
  .badge-row {{
    display: flex;
    align-items: flex-start;
    margin: 10px 0;
  }}
  .badge-circle {{
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background-color: #00A3E0;
    color: #ffffff;
    font-weight: bold;
    font-size: 11pt;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 14px;
    flex-shrink: 0;
    box-shadow: 0 2px 4px rgba(0,163,224,0.3);
  }}
  .badge-content {{
    flex-grow: 1;
  }}
  .badge-title {{
    font-size: 12pt;
    font-weight: bold;
    color: #003B71;
    margin-bottom: 4px;
  }}

  /* Outcome Box from image */
  .outcome-box {{
    background: #EBF7FD;
    border: 1.5px dashed #00A3E0;
    border-radius: 6px;
    padding: 10px 16px;
    text-align: center;
    color: #003B71;
    font-size: 9.5pt;
    font-weight: 600;
    margin-top: 14px;
  }}

  /* Modern Content Cards */
  .card {{
    background: #ffffff;
    border: 1px solid #D0EBF8;
    border-radius: 5px;
    padding: 10px 14px;
    margin-bottom: 10px;
    box-shadow: 0 1px 3px rgba(0,59,113,0.04);
  }}
  .card-cyan {{
    background: #F7FCFE;
    border-left: 4px solid #00A3E0;
  }}
  .card-navy {{
    background: #F4F8FC;
    border-left: 4px solid #003B71;
  }}

  /* Tables */
  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 10px 0;
    font-size: 8.5pt;
  }}
  th, td {{
    border: 1px solid #D0EBF8;
    padding: 6px 9px;
    text-align: left;
    vertical-align: middle;
  }}
  th {{
    background-color: #003B71;
    color: #ffffff;
    font-weight: bold;
  }}
  tr:nth-child(even) {{
    background-color: #F8FCFE;
  }}

  /* Code snippet block */
  pre.code-block {{
    background-color: #0F172A;
    color: #E2E8F0;
    font-family: 'Liberation Mono', 'Courier New', monospace;
    font-size: 7.8pt;
    padding: 9px 12px;
    border-radius: 4px;
    border-left: 4px solid #00A3E0;
    line-height: 1.38;
    margin: 8px 0;
    white-space: pre-wrap;
    word-break: break-all;
  }}
  code.inline {{
    background-color: #EBF7FD;
    color: #003B71;
    font-family: 'Liberation Mono', monospace;
    font-size: 8.2pt;
    padding: 1px 4px;
    border-radius: 3px;
    border: 1px solid #D0EBF8;
    font-weight: bold;
  }}

  /* Links */
  a.ref-link {{
    color: #00A3E0;
    text-decoration: none;
    font-weight: bold;
  }}
  a.ref-link:hover {{
    text-decoration: underline;
  }}

  /* Diagrams */
  .diagram-container {{
    text-align: center;
    margin: 10px 0;
  }}
  .diagram-img {{
    max-width: 100%;
    height: auto;
    border: 1px solid #D0EBF8;
    border-radius: 5px;
    background: #ffffff;
  }}
  .diagram-caption {{
    font-size: 7.8pt;
    color: #64748B;
    margin-top: 4px;
    font-style: italic;
  }}

  ul, ol {{
    margin: 0 0 8px 18px;
    padding: 0;
  }}
  li {{
    margin-bottom: 2px;
  }}
  p {{
    margin: 0 0 8px 0;
    text-align: justify;
  }}
</style>
</head>
<body>

  <!-- ========================================================================= -->
  <!-- PAGE 1: What is Zephyr RTOS? -->
  <!-- ========================================================================= -->
  <div class="page-box">
    <div class="logo-header">
      <img src="{ASSETS_DIR}/microchip_logo.png" class="logo-img" alt="Microchip Logo" />
      <img src="{ASSETS_DIR}/zephyr_logo_full.svg" class="logo-img" alt="Zephyr RTOS Logo" />
    </div>

    <div class="title-card">
      <h1 class="page-title">Page 1: What is Zephyr RTOS?</h1>
      <div class="page-subtitle">Introduction, Purpose, Architecture &amp; References</div>
    </div>

    <h2 class="sec-heading">1.1 Understanding Real-Time Operating Systems (RTOS)</h2>
    <p>
      An <strong>RTOS (Real-Time Operating System)</strong> is an operating system engineered to execute instructions with strict, predictable timing. While general-purpose operating systems like Linux or Windows focus on overall data throughput, an RTOS guarantees that time-critical events, hardware interrupts, and sensor data are processed deterministically within exact deadlines.
    </p>

    <h2 class="sec-heading">1.2 About the Zephyr Project</h2>
    <p>
      <strong>Zephyr</strong> is an open-source, vendor-neutral real-time operating system managed by the <strong>Linux Foundation</strong>, licensed under the permissive <strong>Apache 2.0</strong> license. Backed by industry giants including <strong>Microchip, Google, Intel, Nordic Semiconductor, NXP, STMicroelectronics, and Qualcomm</strong>, Zephyr scales from small 32-bit microcontrollers with only 8 KB of RAM up to multi-core MPUs.
    </p>

    <div class="card card-cyan">
      <strong>Core Architectural Pillars of Zephyr:</strong>
      <ul>
        <li><strong>Preemptive Real-Time Kernel:</strong> Deterministic priority-based scheduling, tickless idle mode, semaphores, mutexes, message queues, and memory slabs.</li>
        <li><strong>Devicetree (DTS):</strong> Hardware abstraction borrowed from Linux, decoupling silicon pinouts from C code.</li>
        <li><strong>Kconfig Configuration:</strong> Granular compile-time feature selection to strip unused code and save Flash/RAM.</li>
        <li><strong>Batteries-Included Connectivity:</strong> Native, certified Bluetooth Low Energy (BLE), Wi-Fi, Ethernet, CAN-FD, USB, and OpenThread stacks.</li>
      </ul>
    </div>

    <h2 class="sec-heading">1.3 Why Zephyr for Embedded Systems Education?</h2>
    <p>
      Traditional embedded curricula lock students into vendor-specific bare-metal registers. Zephyr equips students with universal, cross-architecture engineering skills used in modern automotive, medical, industrial, and IoT products.
    </p>

    <h2 class="sec-heading">1.4 Official Referral &amp; Reference Links</h2>
    <table>
      <thead>
        <tr>
          <th>Resource</th>
          <th>URL Link</th>
          <th>Description</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Zephyr Project Home</strong></td>
          <td><a class="ref-link" href="https://zephyrproject.org/">https://zephyrproject.org/</a></td>
          <td>Official website, release notes, and community links</td>
        </tr>
        <tr>
          <td><strong>Zephyr Documentation</strong></td>
          <td><a class="ref-link" href="https://docs.zephyrproject.org/">https://docs.zephyrproject.org/</a></td>
          <td>Comprehensive APIs, driver guides, and sample codes</td>
        </tr>
        <tr>
          <td><strong>Linux Foundation Page</strong></td>
          <td><a class="ref-link" href="https://www.linuxfoundation.org/projects/embedded-iot">https://www.linuxfoundation.org/</a></td>
          <td>Governance, charter, and open-source compliance</td>
        </tr>
        <tr>
          <td><strong>Zephyr GitHub Repository</strong></td>
          <td><a class="ref-link" href="https://github.com/zephyrproject-rtos/zephyr">https://github.com/zephyrproject-rtos/zephyr</a></td>
          <td>Upstream kernel source code, issues, and pull requests</td>
        </tr>
      </tbody>
    </table>
  </div>

  <!-- ========================================================================= -->
  <!-- PAGE 2: Microchip & Zephyr: How They Tie Together -->
  <!-- ========================================================================= -->
  <div class="page-box">
    <div class="logo-header">
      <img src="{ASSETS_DIR}/microchip_logo.png" class="logo-img" alt="Microchip Logo" />
      <img src="{ASSETS_DIR}/zephyr_logo_full.svg" class="logo-img" alt="Zephyr RTOS Logo" />
    </div>

    <div class="title-card">
      <h1 class="page-title">Page 2: Microchip &amp; Zephyr Integration</h1>
      <div class="page-subtitle">How Microchip Brings Upstream Zephyr to Silicon Boards</div>
    </div>

    <h2 class="sec-heading">2.1 The Microchip &amp; Zephyr Partnership</h2>
    <p>
      Microchip Technology is an active member and primary silicon contributor to the Zephyr Project. Rather than requiring users to maintain out-of-tree vendor patches, Microchip directly integrates official silicon drivers, clock generators, and Device Family Packs (DFP) into the upstream Zephyr repository.
    </p>

    <h2 class="sec-heading">2.2 Layered Board Porting Architecture</h2>
    <div class="diagram-container">
      <img src="{ASSETS_DIR}/architecture_diagram.svg" class="diagram-img" style="max-height: 180px;" alt="Microchip Zephyr Architecture" />
      <div class="diagram-caption">Figure 2.1: Microchip Upstream HAL &amp; Zephyr Driver Layering.</div>
    </div>

    <p>Microchip brings Zephyr support to hardware boards through four synchronized layers:</p>
    <ul>
      <li><strong>1. Microchip HAL Module (<code>modules/hal/microchip</code>):</strong> Contains vendor register header files, CMSIS startup vectors, and Device Family Packs (DFP) for PIC32C/SAM devices.</li>
      <li><strong>2. SoC Series Architecture (<code>zephyr/soc/microchip/pic32c</code>):</strong> Configures the 48 MHz FDPLL96M oscillator, Flash Wait States (NVMCTRL), MPU regions, and Power Management.</li>
      <li><strong>3. Device Driver Layer (<code>zephyr/drivers</code>):</strong> Standardized drivers for Microchip PORT (GPIO), SERCOM (UART/I2C/SPI), and ADC peripherals.</li>
      <li><strong>4. Board Target Definition (<code>zephyr/boards/microchip/pic32c/pic32cm_gc00_cpro</code>):</strong> Declares the pinout, chosen serial console, memory partitions, and onboard LEDs/buttons via Devicetree (<code>.dts</code>).</li>
    </ul>

    <h2 class="sec-heading">2.3 Official Microchip Referral &amp; Source Links</h2>
    <table>
      <thead>
        <tr>
          <th>Component</th>
          <th>Official URL / Referral Link</th>
          <th>Repository Path</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Microchip Upstream HAL</strong></td>
          <td><a class="ref-link" href="https://github.com/zephyrproject-rtos/hal_microchip">https://github.com/zephyrproject-rtos/hal_microchip</a></td>
          <td><code>modules/hal/microchip</code></td>
        </tr>
        <tr>
          <td><strong>Microchip 32-bit MCUs</strong></td>
          <td><a class="ref-link" href="https://www.microchip.com/en-us/products/microcontrollers-and-microprocessors/32-bit-mcus">https://www.microchip.com/pic32</a></td>
          <td>Official Silicon Portal</td>
        </tr>
        <tr>
          <td><strong>PIC32CM GC00 Board Docs</strong></td>
          <td><a class="ref-link" href="https://docs.zephyrproject.org/latest/boards/microchip/pic32c/pic32cm_gc00_cpro/doc/index.html">https://docs.zephyrproject.org/.../pic32cm_gc00_cpro</a></td>
          <td><code>boards/microchip/pic32c/pic32cm_gc00_cpro/</code></td>
        </tr>
      </tbody>
    </table>
  </div>

  <!-- ========================================================================= -->
  <!-- PAGE 3: Board Specifications & Peripheral Support -->
  <!-- ========================================================================= -->
  <div class="page-box">
    <div class="logo-header">
      <img src="{ASSETS_DIR}/microchip_logo.png" class="logo-img" alt="Microchip Logo" />
      <img src="{ASSETS_DIR}/zephyr_logo_full.svg" class="logo-img" alt="Zephyr RTOS Logo" />
    </div>

    <div class="title-card">
      <h1 class="page-title">Page 3: Board Specifications &amp; Peripherals</h1>
      <div class="page-subtitle">Hardware Specs &amp; Peripheral Support for PIC32CM GC00 Curiosity Pro</div>
    </div>

    <div class="diagram-container">
      <img src="{ASSETS_DIR}/board.png" class="diagram-img" style="max-height: 150px;" alt="Board Photo" />
      <div class="diagram-caption">Figure 3.1: Microchip PIC32CM GC00 Curiosity Pro Evaluation Kit.</div>
    </div>

    <h2 class="sec-heading">3.1 Hardware Specifications</h2>
    <table>
      <thead>
        <tr>
          <th style="width: 30%;">Parameter</th>
          <th style="width: 35%;">Specification Value</th>
          <th style="width: 35%;">Details &amp; Benefits</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Microcontroller</strong></td>
          <td>PIC32CM5112GC00100</td>
          <td>Microchip 32-bit MCU (100-pin TQFP)</td>
        </tr>
        <tr>
          <td><strong>Processor Core</strong></td>
          <td>ARM Cortex-M23</td>
          <td>ARMv8-M Baseline RISC architecture</td>
        </tr>
        <tr>
          <td><strong>System Frequency</strong></td>
          <td>48.0 MHz FDPLL96M</td>
          <td>Internal high-precision clock generator</td>
        </tr>
        <tr>
          <td><strong>Flash / SRAM</strong></td>
          <td>512 KB Flash / 128 KB SRAM</td>
          <td>Zero-wait-state high speed execution</td>
        </tr>
        <tr>
          <td><strong>Onboard Debugger</strong></td>
          <td>Microchip nEDBG</td>
          <td>CMSIS-DAP debugger &amp; CDC Virtual COM Port</td>
        </tr>
        <tr>
          <td><strong>Operating Voltage</strong></td>
          <td>3.3 V DC</td>
          <td>Supplied via USB or external header</td>
        </tr>
      </tbody>
    </table>

    <h2 class="sec-heading">3.2 Peripheral Support Status in Zephyr</h2>
    <table>
      <thead>
        <tr>
          <th>Peripheral</th>
          <th>Driver / Node Identifier</th>
          <th>Status</th>
          <th>Hardware Mapping</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>GPIO Controller</strong></td>
          <td><code>gpio_mchp_port_g1</code> (PORTA, PORTB)</td>
          <td><strong style="color: #00A3E0;">Supported</strong></td>
          <td>PA20 (LED0), PA18 (LED1), PB07 (SW0), PB11 (SW1)</td>
        </tr>
        <tr>
          <td><strong>UART / Console</strong></td>
          <td><code>uart_mchp_sercom</code></td>
          <td><strong style="color: #00A3E0;">Supported</strong></td>
          <td>PA04 / PA05 (115200 8N1 to EDBG Virtual COM)</td>
        </tr>
        <tr>
          <td><strong>Pin Controller</strong></td>
          <td><code>pinctrl-pic32c</code></td>
          <td><strong style="color: #00A3E0;">Supported</strong></td>
          <td>Dynamic pin multiplexing subsystem</td>
        </tr>
        <tr>
          <td><strong>Core Timer</strong></td>
          <td>ARM Cortex-M SysTick</td>
          <td><strong style="color: #00A3E0;">Supported</strong></td>
          <td>Kernel 1000 Hz system tick for <code>k_msleep()</code></td>
        </tr>
        <tr>
          <td><strong>Flash Controller</strong></td>
          <td><code>nvmctrl</code></td>
          <td><strong style="color: #00A3E0;">Supported</strong></td>
          <td>Boot flash (16KB) &amp; Code partition (496KB)</td>
        </tr>
        <tr>
          <td><strong>ADC / DAC / I2C</strong></td>
          <td>Microchip SERCOM / ADC</td>
          <td>Roadmap</td>
          <td>Available through external overlays</td>
        </tr>
      </tbody>
    </table>
  </div>

  <!-- ========================================================================= -->
  <!-- PAGE 4: Hardware and Software Used (Matching User Image Theme) -->
  <!-- ========================================================================= -->
  <div class="page-box">
    <div class="logo-header">
      <img src="{ASSETS_DIR}/microchip_logo.png" class="logo-img" alt="Microchip Logo" />
      <img src="{ASSETS_DIR}/zephyr_logo_full.svg" class="logo-img" alt="Zephyr RTOS Logo" />
    </div>

    <div class="title-card">
      <h1 class="page-title">Page 4: Development Platform</h1>
      <div class="page-subtitle">Hardware and Software Architecture Overview</div>
    </div>

    <!-- Badge 01: Hardware (Styled after user image) -->
    <div class="badge-row">
      <div class="badge-circle">01</div>
      <div class="badge-content">
        <div class="badge-title">Hardware</div>
        <div class="card card-navy">
          <ul>
            <li><strong>Board:</strong> Microchip PIC32CM GC00 Curiosity Pro (EV33A17A)</li>
            <li><strong>MCU:</strong> PIC32CM5112GC00100 (32-bit ARM Cortex-M23 @ 48 MHz)</li>
            <li><strong>Onboard LED:</strong> Yellow LED0 (Pin PA20, Active-Low) for visual output</li>
            <li><strong>User Pushbuttons:</strong> Mechanical switch SW0 (Pin PB07) for interactive input</li>
            <li><strong>USB Interface:</strong> Micro-USB connection (J100) for programming, debugging, and serial UART telemetry</li>
          </ul>
        </div>
      </div>
    </div>

    <!-- Badge 02: Software (Styled after user image) -->
    <div class="badge-row">
      <div class="badge-circle">02</div>
      <div class="badge-content">
        <div class="badge-title">Software</div>
        <div class="card card-cyan">
          <ul>
            <li><strong>Development IDE:</strong> MPLAB VS Code / Visual Studio Code with Zephyr extensions</li>
            <li><strong>Operating System:</strong> Zephyr RTOS Workspace (v3.7+)</li>
            <li><strong>Build Tool:</strong> West meta-tool (CMake &amp; Ninja automated workflow)</li>
            <li><strong>Compiler Toolchain:</strong> Compatible Zephyr ARM SDK (<code>arm-zephyr-eabi</code>)</li>
            <li><strong>Board Support Package:</strong> Upstream <code>pic32cm_gc00_cpro</code> board target</li>
          </ul>
        </div>
      </div>
    </div>

    <div class="outcome-box">
      <strong>Outcome:</strong> A reliable, standardized environment for developing, building, flashing, and running professional Zephyr RTOS applications on Microchip hardware.
    </div>
  </div>

  <!-- ========================================================================= -->
  <!-- PAGE 5: How to Clone Zephyr Project & Setup Locally -->
  <!-- ========================================================================= -->
  <div class="page-box">
    <div class="logo-header">
      <img src="{ASSETS_DIR}/microchip_logo.png" class="logo-img" alt="Microchip Logo" />
      <img src="{ASSETS_DIR}/zephyr_logo_full.svg" class="logo-img" alt="Zephyr RTOS Logo" />
    </div>

    <div class="title-card">
      <h1 class="page-title">Page 5: Cloning &amp; Local Setup</h1>
      <div class="page-subtitle">How to Clone Zephyr and Initialize Your Local Workspace</div>
    </div>

    <h2 class="sec-heading">5.1 Workspace Folder Architecture</h2>
    <p>
      Zephyr projects are managed using a workspace structure where repositories and modules are coordinated through <code>west</code>.
    </p>

    <h2 class="sec-heading">5.2 Step-by-Step Terminal Instructions</h2>

    <p><strong>Step 1: Create a Dedicated Directory &amp; Virtual Environment</strong></p>
    <pre class="code-block"># Create workspace root directory
mkdir -p ~/zephyrproject &amp;&amp; cd ~/zephyrproject

# Create and activate Python 3 virtual environment
python3 -m venv .venv
source .venv/bin/activate</pre>

    <p><strong>Step 2: Install West (Zephyr's Meta-Tool)</strong></p>
    <pre class="code-block">pip install --upgrade pip
pip install west</pre>

    <p><strong>Step 3: Initialize the Zephyr Manifest Repository</strong></p>
    <pre class="code-block"># Initialize west in the local workspace directory
west init -l zephyr</pre>

    <p><strong>Step 4: Clone External Submodules &amp; Microchip Packs</strong></p>
    <pre class="code-block"># Clones hal_microchip, CMSIS packs, mbedTLS, and tools
west update</pre>

    <p><strong>Step 5: Export CMake Packages &amp; Python Dependencies</strong></p>
    <pre class="code-block"># Register Zephyr CMake packages
west zephyr-export

# Install required Python packages for Zephyr tools
pip install -r zephyr/scripts/requirements.txt</pre>

    <div class="card card-cyan">
      <strong>Pro Tip for Students:</strong> Always ensure your virtual environment is active before running any West commands:
      <code>source ~/zephyrproject/.venv/bin/activate</code>
    </div>
  </div>

  <!-- ========================================================================= -->
  <!-- PAGE 6: Setting Up the Zephyr Environment -->
  <!-- ========================================================================= -->
  <div class="page-box">
    <div class="logo-header">
      <img src="{ASSETS_DIR}/microchip_logo.png" class="logo-img" alt="Microchip Logo" />
      <img src="{ASSETS_DIR}/zephyr_logo_full.svg" class="logo-img" alt="Zephyr RTOS Logo" />
    </div>

    <div class="title-card">
      <h1 class="page-title">Page 6: Environment &amp; Toolchain Setup</h1>
      <div class="page-subtitle">Installing SDK Toolchain, Dependencies &amp; USB Permissions</div>
    </div>

    <h2 class="sec-heading">6.1 Host Operating System Dependencies (Ubuntu / WSL2)</h2>
    <pre class="code-block">sudo apt update &amp;&amp; sudo apt install -y git cmake ninja-build gperf ccache dfu-util \
  device-tree-compiler wget python3-dev python3-pip python3-setuptools xz-utils make gcc</pre>

    <h2 class="sec-heading">6.2 Installing the Zephyr ARM SDK Cross-Compiler</h2>
    <p>
      The <strong>Zephyr SDK</strong> contains cross-compilation toolchains (<code>arm-zephyr-eabi-gcc</code>) required to build ARM Cortex-M binaries on an x86 host PC:
    </p>

    <pre class="code-block"># 1. Download Zephyr SDK archive
cd ~
wget https://github.com/zephyrproject-rtos/sdk-ng/releases/download/v0.16.8/zephyr-sdk-0.16.8_linux-x86_64.tar.xz

# 2. Extract archive
tar xvf zephyr-sdk-0.16.8_linux-x86_64.tar.xz

# 3. Run toolchain installation script for ARM
cd zephyr-sdk-0.16.8
./setup.sh -t arm-zephyr-eabi -h -c</pre>

    <h2 class="sec-heading">6.3 Configuring USB Permissions (udev Rules)</h2>
    <p>
      Linux restricts direct USB access to root by default. Installing Zephyr's udev rules permits regular user access to the onboard Microchip nEDBG programmer:
    </p>

    <pre class="code-block">sudo cp ~/zephyrproject/zephyr/scripts/udev/rules.d/* /etc/udev/rules.d/
sudo udevadm control --reload-rules
sudo udevadm trigger</pre>

    <h2 class="sec-heading">6.4 Verifying the Environment</h2>
    <table style="margin-top: 10px;">
      <thead>
        <tr>
          <th>Verification Command</th>
          <th>Expected Response</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><code>west --version</code></td>
          <td>West version 1.2.0 or newer</td>
        </tr>
        <tr>
          <td><code>arm-zephyr-eabi-gcc --version</code></td>
          <td>arm-zephyr-eabi-gcc 12.2.0 (Zephyr SDK)</td>
        </tr>
        <tr>
          <td><code>cmake --version</code></td>
          <td>CMake version 3.20.0 or higher</td>
        </tr>
      </tbody>
    </table>
  </div>

  <!-- ========================================================================= -->
  <!-- PAGE 7: Explanation of prj.conf, CMakeLists.txt & app.overlay -->
  <!-- ========================================================================= -->
  <div class="page-box">
    <div class="logo-header">
      <img src="{ASSETS_DIR}/microchip_logo.png" class="logo-img" alt="Microchip Logo" />
      <img src="{ASSETS_DIR}/zephyr_logo_full.svg" class="logo-img" alt="Zephyr RTOS Logo" />
    </div>

    <div class="title-card">
      <h1 class="page-title">Page 7: Application Configuration Files</h1>
      <div class="page-subtitle">Deep Dive into CMakeLists.txt, prj.conf, and app.overlay</div>
    </div>

    <h2 class="sec-heading">7.1 CMakeLists.txt — Build Definition</h2>
    <pre class="code-block">cmake_minimum_required(VERSION 3.20.0)
find_package(Zephyr REQUIRED HINTS $ENV{{ZEPHYR_BASE}})
project(pic32cm_gc00_blinky)
target_sources(app PRIVATE src/main.c)</pre>
    <p>
      <code>find_package(Zephyr)</code> resolves board Devicetree files, configures Kconfig options, imports the ARM toolchain, and links the Zephyr RTOS kernel into the executable.
    </p>

    <h2 class="sec-heading">7.2 prj.conf — Kconfig Kernel &amp; Driver Configuration</h2>
    <pre class="code-block">CONFIG_GPIO=y               # Compiles the Microchip PORT GPIO driver
CONFIG_PRINTK=y             # Enables Zephyr's formatted logging system
CONFIG_STDOUT_CONSOLE=y     # Directs C printf() output to the UART serial port</pre>
    <p>
      In Zephyr, drivers are disabled by default to save flash memory. <code>prj.conf</code> enables only what your application requires.
    </p>

    <h2 class="sec-heading">7.3 app.overlay — Custom Devicetree Overlays</h2>
    <p>
      An <strong>overlay file</strong> (<code>app.overlay</code>) allows students to modify or add hardware nodes without modifying the main board Devicetree:
    </p>

    <pre class="code-block">/ {{
    aliases {{
        my-custom-led = &amp;custom_led;
    }};
    leds {{
        compatible = "gpio-leds";
        custom_led: led_custom {{
            gpios = &lt;&amp;porta 18 GPIO_ACTIVE_LOW&gt;;
            label = "Secondary Yellow LED1";
        }};
    }};
}};</pre>

    <div class="card card-navy">
      <strong>Devicetree Rule:</strong> Devicetree maps hardware topology (Pins &rarr; Aliases). C code accesses peripherals via generic aliases like <code>DT_ALIAS(led0)</code>, keeping firmware 100% portable.
    </div>
  </div>

  <!-- ========================================================================= -->
  <!-- PAGE 8: How to Build & Flash Code -->
  <!-- ========================================================================= -->
  <div class="page-box">
    <div class="logo-header">
      <img src="{ASSETS_DIR}/microchip_logo.png" class="logo-img" alt="Microchip Logo" />
      <img src="{ASSETS_DIR}/zephyr_logo_full.svg" class="logo-img" alt="Zephyr RTOS Logo" />
    </div>

    <div class="title-card">
      <h1 class="page-title">Page 8: Building &amp; Flashing Firmware</h1>
      <div class="page-subtitle">Compilation Pipeline, West Commands &amp; Flashing Guide</div>
    </div>

    <h2 class="sec-heading">8.1 The Zephyr Compilation Workflow</h2>
    <div class="diagram-container">
      <img src="{ASSETS_DIR}/flowchart_diagram.svg" class="diagram-img" style="max-height: 170px;" alt="Build Pipeline" />
      <div class="diagram-caption">Figure 8.1: Complete Build &amp; Execution Pipeline.</div>
    </div>

    <h2 class="sec-heading">8.2 Step-by-Step Command Matrix</h2>
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
          <td><strong>Clean Pristine Build</strong></td>
          <td><code>west build -b pic32cm_gc00_cpro pic32cm_gc00_blinky -p always</code></td>
          <td>Discards prior cache, generates new Devicetree headers, compiles all files</td>
        </tr>
        <tr>
          <td><strong>Incremental Build</strong></td>
          <td><code>west build -p auto</code></td>
          <td>Fast compilation recompiling only modified source files</td>
        </tr>
        <tr>
          <td><strong>Flash Hardware</strong></td>
          <td><code>west flash</code></td>
          <td>Invokes J-Link / EDBG to program MCU internal flash over USB</td>
        </tr>
        <tr>
          <td><strong>Flash with J-Link</strong></td>
          <td><code>west flash --runner jlink</code></td>
          <td>Explicitly specifies J-Link runner for Curiosity Pro</td>
        </tr>
      </tbody>
    </table>

    <h2 class="sec-heading">8.3 Generated Build Artifacts</h2>
    <ul>
      <li><code>build/zephyr/zephyr.elf</code>: Complete ELF binary containing symbols and debug tables.</li>
      <li><code>build/zephyr/zephyr.hex</code>: Intel HEX record used by hardware programmers.</li>
      <li><code>build/zephyr/zephyr.bin</code>: Raw flat machine code image programmed into internal Flash memory.</li>
    </ul>
  </div>

  <!-- ========================================================================= -->
  <!-- PAGE 9: Serial Output & Timing Specifications -->
  <!-- ========================================================================= -->
  <div class="page-box">
    <div class="logo-header">
      <img src="{ASSETS_DIR}/microchip_logo.png" class="logo-img" alt="Microchip Logo" />
      <img src="{ASSETS_DIR}/zephyr_logo_full.svg" class="logo-img" alt="Zephyr RTOS Logo" />
    </div>

    <div class="title-card">
      <h1 class="page-title">Page 9: Serial Telemetry &amp; Timing</h1>
      <div class="page-subtitle">UART Output Logs, Timing Waveform &amp; Electrical Logic</div>
    </div>

    <h2 class="sec-heading">9.1 Serial Console Connection (115200 8N1)</h2>
    <p>
      Connect to the USB CDC Virtual COM port exposed by the onboard debugger:
    </p>
    <pre class="code-block"># Connect via picocom on Linux
picocom -b 115200 /dev/ttyACM0</pre>

    <h2 class="sec-heading">9.2 Expected Serial Output Log</h2>
    <pre class="code-block">*** Booting Zephyr OS build v3.7.0 ***
Iteration 1/5 - LED state: ON (350 ms ON)
Iteration 1/5 - LED state: OFF (450 ms OFF)
Iteration 2/5 - LED state: ON (350 ms ON)
Iteration 2/5 - LED state: OFF (450 ms OFF)
Iteration 3/5 - LED state: ON (350 ms ON)
Iteration 3/5 - LED state: OFF (450 ms OFF)
Iteration 4/5 - LED state: ON (350 ms ON)
Iteration 4/5 - LED state: OFF (450 ms OFF)
Iteration 5/5 - LED state: ON (350 ms ON)
Iteration 5/5 - LED state: OFF (450 ms OFF)
Pause - LED state: OFF (1000 ms Pause)

Iteration 1/5 - LED state: ON (350 ms ON)
...</pre>

    <h2 class="sec-heading">9.3 Accurate Timing Waveform Analysis</h2>
    <div class="diagram-container">
      <img src="{ASSETS_DIR}/timing_waveform.svg" class="diagram-img" alt="Timing Waveform" />
      <div class="diagram-caption">Figure 9.1: Deterministic 5-Burst Active Pulse &amp; 1000 ms Quiescent Rest Waveform.</div>
    </div>
  </div>

  <!-- ========================================================================= -->
  <!-- PAGE 10: Conclusion & Student Lab Challenges -->
  <!-- ========================================================================= -->
  <div class="page-box">
    <div class="logo-header">
      <img src="{ASSETS_DIR}/microchip_logo.png" class="logo-img" alt="Microchip Logo" />
      <img src="{ASSETS_DIR}/zephyr_logo_full.svg" class="logo-img" alt="Zephyr RTOS Logo" />
    </div>

    <div class="title-card">
      <h1 class="page-title">Page 10: Conclusion &amp; Lab Exercises</h1>
      <div class="page-subtitle">Summary, Student Exercises &amp; Official References</div>
    </div>

    <h2 class="sec-heading">10.1 Key Learning Summary</h2>
    <ul>
      <li><strong>Standardized Driver Interfaces:</strong> The application calls <code>gpio_pin_set_dt()</code> and <code>k_msleep()</code>, which run identically on any Zephyr-supported microcontroller.</li>
      <li><strong>Electrical Logic Abstraction:</strong> Zephyr automatically translates logical states into physical voltage levels based on Devicetree polarity flags (<code>GPIO_ACTIVE_LOW</code>).</li>
      <li><strong>Tickless Power Savings:</strong> <code>k_msleep()</code> allows the ARM Cortex-M23 core to enter low-power sleep between LED pulses.</li>
    </ul>

    <h2 class="sec-heading">10.2 Student Lab Challenges</h2>
    <div class="card card-cyan">
      <strong>Challenge 1: Morse Code SOS Transmitter</strong>
      <p style="margin: 3px 0 0 0;">Modify the delay constants to transmit international Morse code SOS on LED0 (3 short pulses of 150 ms, 3 long pulses of 450 ms, 3 short pulses of 150 ms, followed by a 2000 ms pause).</p>
    </div>

    <div class="card card-navy">
      <strong>Challenge 2: Dual Alternating Beacon Flasher</strong>
      <p style="margin: 3px 0 0 0;">Add secondary LED1 on pin PA18 using <code>DT_ALIAS(led1)</code>. Alternate LED0 and LED1 like an emergency responder light bar.</p>
    </div>

    <div class="card card-cyan">
      <strong>Challenge 3: Pushbutton-Gated Pattern</strong>
      <p style="margin: 3px 0 0 0;">Read mechanical switch SW0 on pin PB07 using <code>DT_ALIAS(sw0)</code>. Only execute the 5-burst blinking sequence when SW0 is held down.</p>
    </div>

    <h2 class="sec-heading">10.3 Official References &amp; Links</h2>
    <table style="margin-top: 6px;">
      <thead>
        <tr>
          <th>Portal</th>
          <th>URL</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Microchip Official</td>
          <td><a class="ref-link" href="https://www.microchip.com">https://www.microchip.com</a></td>
        </tr>
        <tr>
          <td>Zephyr Project</td>
          <td><a class="ref-link" href="https://zephyrproject.org">https://zephyrproject.org</a></td>
        </tr>
        <tr>
          <td>Project GitHub</td>
          <td><a class="ref-link" href="https://github.com/sujandurai/pic32cm_gc00_blinky">https://github.com/sujandurai/pic32cm_gc00_blinky</a></td>
        </tr>
      </tbody>
    </table>

    <div class="outcome-box" style="margin-top: 10px;">
      Congratulations on mastering Zephyr RTOS fundamentals on Microchip PIC32CM hardware!
    </div>
  </div>

</body>
</html>
"""

temp_html = "/tmp/zephyr_10page_guide.html"
with open(temp_html, "w", encoding="utf-8") as f:
    f.write(html_content)

print("HTML written to:", temp_html)
print("Rendering 10-page PDF via WeasyPrint...")
weasyprint.HTML(temp_html).write_pdf(OUTPUT_PDF)
print("Output PDF:", OUTPUT_PDF)

shutil.copyfile(OUTPUT_PDF, COPY_ROOT_PDF)
print("Copied to workspace root:", COPY_ROOT_PDF)
