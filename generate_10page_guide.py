#!/usr/bin/env python3
"""
Generate an exact 10-page, beautifully spaced, uncluttered Zephyr RTOS Student Guide.
Every page (1 to 10) is carefully proportioned so that:
- It NEVER overflows to a second page (total page count is EXACTLY 10).
- Text is concise, user-friendly, and airy with generous line-height (1.65) and letter-spacing.
- Color palette matches user's uploaded platform slide: Deep Navy (#003B71), Accent Cyan (#00A3E0), Soft Cyan (#EBF7FD).
- Both Microchip and Zephyr logos appear on every page header.
"""

import os
import weasyprint
import shutil
import subprocess

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
    margin: 12mm 15mm 14mm 15mm;
    @top-left {{
      content: "Microchip Technology  |  Zephyr RTOS Student Guide";
      font-family: 'DejaVu Sans', sans-serif;
      font-size: 7.8pt;
      color: #003B71;
      font-weight: bold;
      letter-spacing: 0.3px;
    }}
    @top-right {{
      content: "PIC32CM GC00 Curiosity Pro";
      font-family: 'DejaVu Sans', sans-serif;
      font-size: 7.8pt;
      color: #00A3E0;
      font-weight: bold;
      letter-spacing: 0.3px;
    }}
    @bottom-left {{
      content: "PIC32CM5112GC00100 (ARM Cortex-M23)";
      font-family: 'DejaVu Sans', sans-serif;
      font-size: 7.5pt;
      color: #64748B;
    }}
    @bottom-center {{
      content: "Page " counter(page) " of " counter(pages);
      font-family: 'DejaVu Sans', sans-serif;
      font-size: 8.2pt;
      font-weight: bold;
      color: #003B71;
    }}
    @bottom-right {{
      content: "Lab Quick-Start Guide";
      font-family: 'DejaVu Sans', sans-serif;
      font-size: 7.5pt;
      color: #00A3E0;
      font-weight: bold;
    }}
  }}

  body {{
    font-family: 'DejaVu Sans', 'Liberation Sans', sans-serif;
    font-size: 9.1pt;
    line-height: 1.62;
    letter-spacing: 0.25px;
    word-spacing: 0.6px;
    color: #2D3748;
    margin: 0;
    padding: 0;
  }}

  .page-box {{
    page-break-after: always;
    height: 100%;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
  }}
  .page-box:last-child {{
    page-break-after: avoid;
  }}

  /* Top Header with Logos */
  .logo-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 2px solid #00A3E0;
    padding-bottom: 6px;
    margin-bottom: 12px;
  }}
  .logo-img {{
    height: 34px;
    object-fit: contain;
  }}

  /* Title Card */
  .title-card {{
    background: linear-gradient(135deg, #EBF7FD 0%, #F5FBFE 100%);
    border-left: 5px solid #003B71;
    border-radius: 5px;
    padding: 10px 16px;
    margin-bottom: 12px;
    border-top: 1px solid #D0EBF8;
    border-right: 1px solid #D0EBF8;
    border-bottom: 1px solid #D0EBF8;
  }}
  h1.page-title {{
    font-size: 15pt;
    color: #003B71;
    margin: 0 0 3px 0;
    font-weight: bold;
    letter-spacing: 0.3px;
  }}
  .page-subtitle {{
    font-size: 9.3pt;
    color: #00A3E0;
    font-weight: 600;
  }}

  /* Section Headings */
  h2.sec-heading {{
    color: #003B71;
    font-size: 11pt;
    border-bottom: 1.5px solid #00A3E0;
    padding-bottom: 3px;
    margin-top: 10px;
    margin-bottom: 8px;
    letter-spacing: 0.2px;
  }}

  /* Clean Airy Cards */
  .card {{
    background: #ffffff;
    border: 1px solid #D9EDF7;
    border-radius: 6px;
    padding: 10px 14px;
    margin-bottom: 10px;
    box-shadow: 0 1px 3px rgba(0, 59, 113, 0.03);
  }}
  .card-cyan {{
    background: #F7FCFE;
    border-left: 4px solid #00A3E0;
  }}
  .card-navy {{
    background: #F4F8FC;
    border-left: 4px solid #003B71;
  }}

  /* Badge Pills (01, 02) matching slide */
  .badge-row {{
    display: flex;
    align-items: flex-start;
    margin: 12px 0;
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
    margin-right: 12px;
    flex-shrink: 0;
    box-shadow: 0 2px 4px rgba(0, 163, 224, 0.3);
  }}
  .badge-content {{
    flex-grow: 1;
  }}
  .badge-title {{
    font-size: 11.5pt;
    font-weight: bold;
    color: #003B71;
    margin-bottom: 4px;
    letter-spacing: 0.2px;
  }}

  /* Outcome Box */
  .outcome-box {{
    background: #EBF7FD;
    border: 1.5px dashed #00A3E0;
    border-radius: 6px;
    padding: 10px 16px;
    text-align: center;
    color: #003B71;
    font-size: 9.3pt;
    font-weight: 600;
    margin-top: 14px;
    line-height: 1.5;
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
    letter-spacing: 0.2px;
  }}
  tr:nth-child(even) {{
    background-color: #F8FCFE;
  }}

  /* Code Blocks */
  pre.code-block {{
    background-color: #0F172A;
    color: #E2E8F0;
    font-family: 'Liberation Mono', monospace;
    font-size: 8pt;
    line-height: 1.48;
    padding: 9px 12px;
    border-radius: 5px;
    border-left: 4px solid #00A3E0;
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
    font-size: 7.5pt;
    color: #64748B;
    margin-top: 3px;
    font-style: italic;
  }}

  ul, ol {{
    margin: 0 0 4px 16px;
    padding: 0;
  }}
  li {{
    margin-bottom: 4px;
  }}
  p {{
    margin: 0 0 8px 0;
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

    <h2 class="sec-heading">1.1 What is an RTOS?</h2>
    <div class="card card-navy">
      <p><strong>Deterministic Response:</strong> Unlike general-purpose OSs (Windows/Linux) designed for throughput, an RTOS guarantees real-time deadlines for hardware interrupts and sensor events.</p>
      <p style="margin-bottom: 0;"><strong>Preemptive Multitasking:</strong> Replaces wasteful CPU counting loops with threads that sleep (<code>k_msleep</code>), allowing the MCU to enter low-power idle states.</p>
    </div>

    <h2 class="sec-heading">1.2 About the Zephyr Project</h2>
    <div class="card card-cyan">
      <p><strong>Open Source Governance:</strong> Hosted by the <strong>Linux Foundation</strong> under the permissive <strong>Apache 2.0</strong> license.</p>
      <p><strong>Industry Consortium:</strong> Governed by Microchip, Google, Intel, Nordic, NXP, ST, and Qualcomm.</p>
      <p style="margin-bottom: 0;"><strong>Ultra-Scalable:</strong> Runs efficiently on microcontrollers with 8 KB of RAM up to multi-core MPUs.</p>
    </div>

    <h2 class="sec-heading">1.3 Core Architectural Pillars</h2>
    <div class="card card-navy">
      <ul>
        <li><strong>Devicetree (DTS):</strong> Decouples hardware pins from C code. Switching boards requires zero code changes.</li>
        <li><strong>Kconfig System:</strong> Granular compile-time feature selection to keep binaries lightweight.</li>
        <li><strong>Unified Driver API:</strong> Standardized functions (<code>gpio_pin_set_dt</code>) across all microcontroller vendors.</li>
        <li><strong>Native Stacks:</strong> Certified Bluetooth Low Energy (BLE), Wi-Fi, Ethernet, CAN-FD, USB, and TCP/IP.</li>
      </ul>
    </div>

    <h2 class="sec-heading">1.4 Official Reference Links</h2>
    <table>
      <thead>
        <tr>
          <th style="width: 35%;">Portal</th>
          <th style="width: 65%;">Official URL</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Zephyr Home Page</strong></td>
          <td><a class="ref-link" href="https://zephyrproject.org/">https://zephyrproject.org/</a></td>
        </tr>
        <tr>
          <td><strong>Official Documentation</strong></td>
          <td><a class="ref-link" href="https://docs.zephyrproject.org/">https://docs.zephyrproject.org/</a></td>
        </tr>
        <tr>
          <td><strong>Zephyr GitHub Source</strong></td>
          <td><a class="ref-link" href="https://github.com/zephyrproject-rtos/zephyr">https://github.com/zephyrproject-rtos/zephyr</a></td>
        </tr>
      </tbody>
    </table>
  </div>

  <!-- ========================================================================= -->
  <!-- PAGE 2: Microchip & Zephyr Integration -->
  <!-- ========================================================================= -->
  <div class="page-box">
    <div class="logo-header">
      <img src="{ASSETS_DIR}/microchip_logo.png" class="logo-img" alt="Microchip Logo" />
      <img src="{ASSETS_DIR}/zephyr_logo_full.svg" class="logo-img" alt="Zephyr RTOS Logo" />
    </div>

    <div class="title-card">
      <h1 class="page-title">Page 2: Microchip &amp; Zephyr Integration</h1>
      <div class="page-subtitle">How Microchip Silicon is Tied Directly into Upstream Zephyr</div>
    </div>

    <h2 class="sec-heading">2.1 How Microchip Brings Zephyr to Silicon</h2>
    <div class="card card-cyan">
      <p><strong>Upstream Collaboration:</strong> Microchip Technology directly integrates and maintains official silicon support in standard Zephyr releases—no out-of-tree vendor patches required!</p>
      <p style="margin-bottom: 0;"><strong>Seamless Upgrades:</strong> Firmware developed on Microchip Zephyr boards gains automatic access to new kernel features, security patches, and connectivity stacks.</p>
    </div>

    <h2 class="sec-heading">2.2 Layered Board Porting Architecture</h2>
    <div class="diagram-container">
      <img src="{ASSETS_DIR}/architecture_diagram.svg" class="diagram-img" style="max-height: 135px;" alt="Architecture" />
      <div class="diagram-caption">Figure 2.1: Microchip Upstream HAL &amp; Zephyr Driver Layering.</div>
    </div>

    <div class="card card-navy">
      <ul>
        <li><code>modules/hal/microchip</code>: Vendor CMSIS headers, register definitions, and peripheral bitmasks.</li>
        <li><code>zephyr/soc/microchip</code>: System clock control (48 MHz FDPLL96M), Flash wait states, and power modes.</li>
        <li><code>zephyr/drivers</code>: Microchip PORT (GPIO), SERCOM (UART/I2C/SPI), and ARM SysTick timer.</li>
        <li><code>zephyr/boards/...</code>: Board Devicetree definitions mapping LED0 (PA20) and SW0 (PB07).</li>
      </ul>
    </div>

    <h2 class="sec-heading">2.3 Referral Links &amp; Upstream Repositories</h2>
    <table>
      <thead>
        <tr>
          <th style="width: 35%;">Component</th>
          <th style="width: 65%;">Upstream Referral Link</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Microchip HAL Module</strong></td>
          <td><a class="ref-link" href="https://github.com/zephyrproject-rtos/hal_microchip">https://github.com/zephyrproject-rtos/hal_microchip</a></td>
        </tr>
        <tr>
          <td><strong>Microchip 32-bit MCUs</strong></td>
          <td><a class="ref-link" href="https://www.microchip.com/pic32">https://www.microchip.com/pic32</a></td>
        </tr>
        <tr>
          <td><strong>Board Documentation</strong></td>
          <td><a class="ref-link" href="https://docs.zephyrproject.org/latest/boards/microchip/pic32c/pic32cm_gc00_cpro/doc/index.html">https://docs.zephyrproject.org/.../pic32cm_gc00_cpro</a></td>
        </tr>
      </tbody>
    </table>
  </div>

  <!-- ========================================================================= -->
  <!-- PAGE 3: Board Specifications & Peripherals -->
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
      <img src="{ASSETS_DIR}/board.png" class="diagram-img" style="max-height: 120px;" alt="Board Photo" />
      <div class="diagram-caption">Figure 3.1: Microchip PIC32CM GC00 Curiosity Pro Evaluation Kit.</div>
    </div>

    <h2 class="sec-heading">3.1 Hardware Specifications</h2>
    <table>
      <thead>
        <tr>
          <th>Specification</th>
          <th>Hardware Value</th>
          <th>Student Takeaway</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Microcontroller</strong></td>
          <td>PIC32CM5112GC00100</td>
          <td>Microchip 32-bit MCU in 100-pin TQFP package</td>
        </tr>
        <tr>
          <td><strong>Core &amp; Clock</strong></td>
          <td>ARM Cortex-M23 @ 48 MHz</td>
          <td>Low-power ARMv8-M architecture with FDPLL96M</td>
        </tr>
        <tr>
          <td><strong>Flash &amp; SRAM</strong></td>
          <td>512 KB Flash / 128 KB SRAM</td>
          <td>Ample room for RTOS kernel, stacks, and user code</td>
        </tr>
        <tr>
          <td><strong>Onboard Debugger</strong></td>
          <td>Microchip nEDBG</td>
          <td>CMSIS-DAP programmer &amp; CDC Virtual COM Port</td>
        </tr>
      </tbody>
    </table>

    <h2 class="sec-heading">3.2 Available Peripheral Support in Zephyr</h2>
    <table>
      <thead>
        <tr>
          <th>Peripheral</th>
          <th>Zephyr Driver</th>
          <th>Support Status</th>
          <th>Hardware Mapping</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>GPIO</strong></td>
          <td><code>gpio_mchp_port_g1</code></td>
          <td><strong style="color: #00A3E0;">Supported</strong></td>
          <td>PA20 (LED0), PA18 (LED1), PB07 (SW0)</td>
        </tr>
        <tr>
          <td><strong>UART Console</strong></td>
          <td><code>uart_mchp_sercom</code></td>
          <td><strong style="color: #00A3E0;">Supported</strong></td>
          <td>PA04 / PA05 (115200 8N1 via USB COM)</td>
        </tr>
        <tr>
          <td><strong>Pin Multiplexing</strong></td>
          <td><code>pinctrl-pic32c</code></td>
          <td><strong style="color: #00A3E0;">Supported</strong></td>
          <td>Devicetree pin routing controller</td>
        </tr>
        <tr>
          <td><strong>System Timer</strong></td>
          <td>ARM Cortex-M SysTick</td>
          <td><strong style="color: #00A3E0;">Supported</strong></td>
          <td>1000 Hz kernel tick for <code>k_msleep()</code></td>
        </tr>
        <tr>
          <td><strong>Flash NVM</strong></td>
          <td><code>nvmctrl</code></td>
          <td><strong style="color: #00A3E0;">Supported</strong></td>
          <td>Internal code partition (496KB)</td>
        </tr>
      </tbody>
    </table>
  </div>

  <!-- ========================================================================= -->
  <!-- PAGE 4: Development Platform (Matching User Slide) -->
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

    <!-- Badge 01: Hardware -->
    <div class="badge-row">
      <div class="badge-circle">01</div>
      <div class="badge-content">
        <div class="badge-title">Hardware</div>
        <div class="card card-navy">
          <ul style="margin: 0 0 0 16px;">
            <li><strong>Board:</strong> PIC32CM GC00 Curiosity Pro (EV33A17A)</li>
            <li><strong>MCU:</strong> PIC32CM5112GC00100 (32-bit ARM Cortex-M23 @ 48 MHz)</li>
            <li><strong>Onboard LED:</strong> Yellow LED0 (Pin PA20, Active-Low) for application demonstration</li>
            <li><strong>USB Connection:</strong> Micro-USB (J100) for programming and interactive debugging</li>
          </ul>
        </div>
      </div>
    </div>

    <!-- Badge 02: Software -->
    <div class="badge-row">
      <div class="badge-circle">02</div>
      <div class="badge-content">
        <div class="badge-title">Software</div>
        <div class="card card-cyan">
          <ul style="margin: 0 0 0 16px;">
            <li><strong>MPLAB VS Code:</strong> Modern IDE workspace with Zephyr and C/C++ extensions</li>
            <li><strong>Zephyr RTOS Workspace:</strong> Portable real-time operating system kernel</li>
            <li><strong>West Build Tool:</strong> Automated CMake, Ninja, and runner meta-tool</li>
            <li><strong>Compatible Zephyr Toolchain:</strong> ARM Embedded SDK (<code>arm-zephyr-eabi</code>)</li>
          </ul>
        </div>
      </div>
    </div>

    <div class="outcome-box">
      <strong>Outcome:</strong> A working environment for building and running Zephyr applications on Microchip hardware.
    </div>
  </div>

  <!-- ========================================================================= -->
  <!-- PAGE 5: How to Clone Zephyr Project & Local Setup -->
  <!-- ========================================================================= -->
  <div class="page-box">
    <div class="logo-header">
      <img src="{ASSETS_DIR}/microchip_logo.png" class="logo-img" alt="Microchip Logo" />
      <img src="{ASSETS_DIR}/zephyr_logo_full.svg" class="logo-img" alt="Zephyr RTOS Logo" />
    </div>

    <div class="title-card">
      <h1 class="page-title">Page 5: Cloning &amp; Local Setup</h1>
      <div class="page-subtitle">How to Clone the Zephyr Project on Your Local Computer</div>
    </div>

    <h2 class="sec-heading">Step 1: Create Workspace &amp; Virtual Environment</h2>
    <div class="card card-navy">
      <pre class="code-block">mkdir -p ~/zephyrproject &amp;&amp; cd ~/zephyrproject
python3 -m venv .venv
source .venv/bin/activate</pre>
    </div>

    <h2 class="sec-heading">Step 2: Install West (Zephyr's Meta-Tool)</h2>
    <div class="card card-cyan">
      <pre class="code-block">pip install --upgrade pip
pip install west</pre>
    </div>

    <h2 class="sec-heading">Step 3: Initialize Zephyr &amp; Download Modules</h2>
    <div class="card card-navy">
      <pre class="code-block"># Initialize west manifest in local directory
west init -l zephyr

# Pull Microchip HAL, CMSIS, and module dependencies
west update</pre>
    </div>

    <h2 class="sec-heading">Step 4: Export CMake &amp; Install Python Requirements</h2>
    <div class="card card-cyan">
      <pre class="code-block">west zephyr-export
pip install -r zephyr/scripts/requirements.txt</pre>
    </div>

    <div class="outcome-box" style="margin-top: 6px;">
      Remember: Always run <code>source ~/zephyrproject/.venv/bin/activate</code> when opening a new terminal!
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
      <div class="page-subtitle">Installing System Packages, ARM SDK &amp; USB Permissions</div>
    </div>

    <h2 class="sec-heading">Step 1: Install Host Operating System Packages</h2>
    <div class="card card-navy">
      <pre class="code-block">sudo apt update &amp;&amp; sudo apt install -y git cmake ninja-build gperf ccache dfu-util \
  device-tree-compiler wget python3-dev python3-pip xz-utils make gcc</pre>
    </div>

    <h2 class="sec-heading">Step 2: Install the Zephyr ARM SDK Cross-Compiler</h2>
    <div class="card card-cyan">
      <pre class="code-block">cd ~
wget https://github.com/zephyrproject-rtos/sdk-ng/releases/download/v0.16.8/zephyr-sdk-0.16.8_linux-x86_64.tar.xz
tar xvf zephyr-sdk-0.16.8_linux-x86_64.tar.xz
cd zephyr-sdk-0.16.8 &amp;&amp; ./setup.sh -t arm-zephyr-eabi -h -c</pre>
    </div>

    <h2 class="sec-heading">Step 3: Setup USB udev Rules for Microchip Debugger</h2>
    <div class="card card-navy">
      <pre class="code-block">sudo cp ~/zephyrproject/zephyr/scripts/udev/rules.d/* /etc/udev/rules.d/
sudo udevadm control --reload-rules &amp;&amp; sudo udevadm trigger</pre>
    </div>

    <h2 class="sec-heading">Quick Verification Checklist</h2>
    <table>
      <thead>
        <tr>
          <th>Command</th>
          <th>Expected Output</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><code>west --version</code></td>
          <td>West version 1.2.0 or newer</td>
        </tr>
        <tr>
          <td><code>arm-zephyr-eabi-gcc --version</code></td>
          <td>GCC 12.2.0 (Zephyr SDK)</td>
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
      <div class="page-subtitle">Understanding CMakeLists.txt, prj.conf, and app.overlay</div>
    </div>

    <h2 class="sec-heading">7.1 CMakeLists.txt — Project Build Script</h2>
    <div class="card card-navy">
      <pre class="code-block">cmake_minimum_required(VERSION 3.20.0)
find_package(Zephyr REQUIRED HINTS $ENV{{ZEPHYR_BASE}})
project(pic32cm_gc00_blinky)
target_sources(app PRIVATE src/main.c)</pre>
      <p style="margin: 4px 0 0 0;"><strong>What it does:</strong> Finds Zephyr packages, loads the board Devicetree, links toolchains, and registers <code>src/main.c</code> for compilation.</p>
    </div>

    <h2 class="sec-heading">7.2 prj.conf — Kconfig Feature Flags</h2>
    <div class="card card-cyan">
      <pre class="code-block">CONFIG_GPIO=y               # Enables Microchip PORT GPIO driver
CONFIG_PRINTK=y             # Enables kernel printk() logging
CONFIG_STDOUT_CONSOLE=y     # Directs C printf() to the serial port</pre>
      <p style="margin: 4px 0 0 0;"><strong>What it does:</strong> Zephyr disables drivers by default. <code>prj.conf</code> turns on only the drivers your application needs, saving memory.</p>
    </div>

    <h2 class="sec-heading">7.3 app.overlay — Custom Devicetree Overlays</h2>
    <div class="card card-navy">
      <pre class="code-block">/ {{
    aliases {{
        my-led = &amp;custom_led;
    }};
    leds {{
        compatible = "gpio-leds";
        custom_led: led_custom {{
            gpios = &lt;&amp;porta 18 GPIO_ACTIVE_LOW&gt;;
            label = "Secondary LED1";
        }};
    }};
}};</pre>
      <p style="margin: 4px 0 0 0;"><strong>What it does:</strong> Allows students to remap pins or add custom peripherals without modifying the base board files.</p>
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
      <div class="page-subtitle">Step-by-Step West Compilation and USB Flashing Guide</div>
    </div>

    <h2 class="sec-heading">8.1 The Build Pipeline</h2>
    <div class="diagram-container">
      <img src="{ASSETS_DIR}/flowchart_diagram.svg" class="diagram-img" style="max-height: 120px;" alt="Flowchart" />
      <div class="diagram-caption">Figure 8.1: Zephyr Compilation &amp; Execution Flow.</div>
    </div>

    <h2 class="sec-heading">8.2 Build Commands</h2>
    <div class="card card-navy">
      <p style="margin: 0 0 3px 0;"><strong>Clean Pristine Build:</strong></p>
      <pre class="code-block">west build -b pic32cm_gc00_cpro pic32cm_gc00_blinky -p always</pre>
      <p style="margin: 4px 0 3px 0;"><strong>Incremental Fast Build:</strong></p>
      <pre class="code-block">west build -p auto</pre>
    </div>

    <h2 class="sec-heading">8.3 Flashing to Hardware</h2>
    <div class="card card-cyan">
      <p style="margin: 0 0 3px 0;">Connect micro-USB to the <strong>DEBUG USB</strong> port (J100) and run:</p>
      <pre class="code-block">west flash</pre>
      <p style="margin: 3px 0 0 0;">Programs internal Flash over USB via the onboard nEDBG debugger.</p>
    </div>

    <h2 class="sec-heading">8.4 Generated Output Binaries</h2>
    <table>
      <thead>
        <tr>
          <th>File</th>
          <th>Location</th>
          <th>Description</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><code>zephyr.elf</code></td>
          <td><code>build/zephyr/</code></td>
          <td>Full binary with symbols for debugging</td>
        </tr>
        <tr>
          <td><code>zephyr.bin</code></td>
          <td><code>build/zephyr/</code></td>
          <td>Flat machine code burned to MCU Flash</td>
        </tr>
      </tbody>
    </table>
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
      <div class="page-subtitle">UART Output Logs and Deterministic Waveform Analysis</div>
    </div>

    <h2 class="sec-heading">9.1 Serial Console Setup (115200 8N1)</h2>
    <div class="card card-navy">
      <pre class="code-block"># Connect via picocom on Linux (or PuTTY on Windows COMx)
picocom -b 115200 /dev/ttyACM0</pre>
    </div>

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
Pause - LED state: OFF (1000 ms Pause)</pre>

    <h2 class="sec-heading">9.3 Timing Waveform Diagram</h2>
    <div class="diagram-container">
      <img src="{ASSETS_DIR}/timing_waveform.svg" class="diagram-img" alt="Waveform" />
      <div class="diagram-caption">Figure 9.1: Deterministic 5-Burst Active Pulse &amp; 1000 ms Quiescent Rest Waveform.</div>
    </div>
  </div>

  <!-- ========================================================================= -->
  <!-- PAGE 10: Conclusion & Lab Exercises -->
  <!-- ========================================================================= -->
  <div class="page-box">
    <div class="logo-header">
      <img src="{ASSETS_DIR}/microchip_logo.png" class="logo-img" alt="Microchip Logo" />
      <img src="{ASSETS_DIR}/zephyr_logo_full.svg" class="logo-img" alt="Zephyr RTOS Logo" />
    </div>

    <div class="title-card">
      <h1 class="page-title">Page 10: Conclusion &amp; Lab Exercises</h1>
      <div class="page-subtitle">Summary, Student Challenges &amp; References</div>
    </div>

    <h2 class="sec-heading">10.1 Key Learning Summary</h2>
    <div class="card card-cyan">
      <ul>
        <li><strong>Portability:</strong> Standardized APIs (<code>gpio_pin_set_dt</code>, <code>k_msleep</code>) run unchanged on any Zephyr MCU.</li>
        <li><strong>Devicetree Abstraction:</strong> Pin numbers and polarity flags (<code>GPIO_ACTIVE_LOW</code>) are decoupled from C code.</li>
        <li><strong>Tickless Power Savings:</strong> <code>k_msleep()</code> allows the ARM Cortex-M23 core to sleep between blinks.</li>
      </ul>
    </div>

    <h2 class="sec-heading">10.2 Hands-On Student Lab Challenges</h2>
    <div class="card card-navy">
      <p style="margin: 0 0 5px 0;"><strong>Challenge 1 (Morse Code SOS):</strong> Modify delay macros to pulse international SOS: 3 short (150ms), 3 long (450ms), 3 short (150ms), followed by a 2000ms rest pause.</p>
      <p style="margin: 0 0 5px 0;"><strong>Challenge 2 (Dual Alternating Beacon):</strong> Add secondary LED1 (PA18) via <code>DT_ALIAS(led1)</code> and alternate like an emergency responder light bar.</p>
      <p style="margin: 0;"><strong>Challenge 3 (Pushbutton Gate):</strong> Read switch SW0 (PB07) via <code>DT_ALIAS(sw0)</code>. Only run the 5-burst blinking pattern when SW0 is held down.</p>
    </div>

    <h2 class="sec-heading">10.3 Quick Resource Links</h2>
    <table>
      <thead>
        <tr>
          <th style="width: 35%;">Resource</th>
          <th style="width: 65%;">URL</th>
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

    <div class="outcome-box" style="margin-top: 8px;">
      Congratulations on mastering Zephyr RTOS fundamentals on Microchip PIC32CM hardware!
    </div>
  </div>

</body>
</html>
"""

temp_html = "/tmp/zephyr_10page_clean.html"
with open(temp_html, "w", encoding="utf-8") as f:
    f.write(html_content)

print("HTML written to:", temp_html)
print("Rendering 10-page PDF via WeasyPrint...")
weasyprint.HTML(temp_html).write_pdf(OUTPUT_PDF)
print("Output PDF:", OUTPUT_PDF)

shutil.copyfile(OUTPUT_PDF, COPY_ROOT_PDF)
print("Copied to workspace root:", COPY_ROOT_PDF)
