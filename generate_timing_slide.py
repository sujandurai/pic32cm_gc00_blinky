import os
import weasyprint
import subprocess

board_img_path = "/home/sujan/zephyrproject/pic32cm_gc00_blinky/assets/board.png"

# Template 1: Exact corrected slide matching user's media_1792558995817.png
html_content_pattern = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  @page {{
    size: 1240px 750px;
    margin: 0;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    background: #f4f8fc;
    width: 1240px;
    height: 750px;
    padding: 16px;
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
    overflow: hidden;
  }}

  /* Decorative background waves */
  .bg-waves {{
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    pointer-events: none;
    z-index: 0;
    opacity: 0.35;
  }}

  .main-card {{
    position: relative;
    z-index: 1;
    width: 1208px;
    height: 718px;
    background: #ffffff;
    border: 1.5px solid #b8daff;
    border-radius: 14px;
    padding: 16px 20px;
    box-shadow: 0 10px 30px rgba(0, 59, 113, 0.08);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}

  /* Header Bar */
  .header-bar {{
    background: #014282;
    border-radius: 7px;
    padding: 10px 22px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    color: #ffffff;
  }}
  .header-title {{
    font-size: 20px;
    font-weight: 700;
    letter-spacing: -0.2px;
    white-space: nowrap;
  }}
  .header-subtitle {{
    font-size: 13.5px;
    color: #d4e8fc;
    font-weight: 400;
    white-space: nowrap;
  }}

  /* Top Section: Timing Pattern */
  .timing-section {{
    background: #edf6fd;
    border: 1.5px solid #bce0fd;
    border-radius: 10px;
    padding: 14px 18px 12px 18px;
    display: flex;
    gap: 16px;
  }}

  .timing-diagram {{
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}

  .pairs-row {{
    display: flex;
    align-items: flex-end;
    gap: 10px;
  }}

  .pair-group {{
    display: flex;
    flex-direction: column;
    align-items: center;
  }}

  .pair-label {{
    font-size: 12px;
    font-weight: 600;
    color: #014282;
    margin-bottom: 3px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }}
  .curly-bracket {{
    width: 86px;
    height: 10px;
    margin-bottom: 2px;
  }}

  .pair-boxes {{
    display: flex;
    gap: 2px;
  }}

  .box {{
    border-radius: 6px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    font-family: inherit;
  }}

  .box-on {{
    width: 45px;
    height: 58px;
    background: #a9e8b7;
    border: 1.5px solid #66bb6a;
  }}
  .box-on .state {{
    font-size: 12.5px;
    font-weight: 700;
    color: #0f5132;
  }}
  .box-on .time {{
    font-size: 10px;
    color: #1b5e20;
    margin-top: 2px;
  }}

  .box-off {{
    width: 45px;
    height: 58px;
    background: #bce3fb;
    border: 1.5px solid #4fc3f7;
  }}
  .box-off .state {{
    font-size: 12.5px;
    font-weight: 700;
    color: #084298;
  }}
  .box-off .time {{
    font-size: 10px;
    color: #0d47a1;
    margin-top: 2px;
  }}

  .box-pause {{
    width: 130px;
    height: 58px;
    background: #cfd8dc;
    border: 1.5px solid #90a4ae;
    margin-left: 2px;
  }}
  .box-pause .state {{
    font-size: 12.5px;
    font-weight: 700;
    color: #263238;
  }}
  .box-pause .time {{
    font-size: 10px;
    color: #37474f;
    margin-top: 2px;
  }}

  /* Dimension lines */
  .dim-line-container {{
    margin-top: 10px;
    display: flex;
    flex-direction: column;
    gap: 6px;
  }}
  .dim-row-1 {{
    display: flex;
    align-items: center;
    font-size: 11px;
    color: #014282;
    font-weight: 600;
  }}
  .dim-arrow-5x {{
    width: 504px;
    display: flex;
    align-items: center;
    gap: 6px;
  }}
  .dim-arrow-pause {{
    width: 130px;
    margin-left: 12px;
    display: flex;
    align-items: center;
    gap: 4px;
    justify-content: center;
  }}

  .dim-row-total {{
    display: flex;
    align-items: center;
    font-size: 12px;
    color: #014282;
    font-weight: 700;
    width: 646px;
    gap: 8px;
  }}

  .arrow-line {{
    flex: 1;
    height: 1px;
    background: #014282;
    position: relative;
  }}
  .arrow-left::before {{
    content: '';
    position: absolute;
    left: 0;
    top: -3px;
    width: 0;
    height: 0;
    border-top: 3.5px solid transparent;
    border-bottom: 3.5px solid transparent;
    border-right: 6px solid #014282;
  }}
  .arrow-right::after {{
    content: '';
    position: absolute;
    right: 0;
    top: -3px;
    width: 0;
    height: 0;
    border-top: 3.5px solid transparent;
    border-bottom: 3.5px solid transparent;
    border-left: 6px solid #014282;
  }}

  /* Legend Box */
  .legend-box {{
    width: 168px;
    background: #ffffff;
    border: 1.5px solid #cce4fc;
    border-radius: 8px;
    padding: 10px 14px;
    display: flex;
    flex-direction: column;
    justify-content: space-around;
  }}
  .legend-item {{
    display: flex;
    align-items: center;
    gap: 10px;
  }}
  .legend-swatch {{
    width: 24px;
    height: 24px;
    border-radius: 4px;
    flex-shrink: 0;
  }}
  .swatch-on {{
    background: #a9e8b7;
    border: 1.5px solid #66bb6a;
  }}
  .swatch-off {{
    background: #bce3fb;
    border: 1.5px solid #4fc3f7;
  }}
  .swatch-pause {{
    background: #cfd8dc;
    border: 1.5px solid #90a4ae;
  }}
  .legend-text {{
    font-size: 11px;
    line-height: 1.25;
  }}
  .legend-text strong {{
    display: block;
    color: #0f172a;
    font-size: 11px;
  }}
  .legend-text span {{
    color: #64748b;
    font-size: 10px;
  }}

  /* Bottom Row Cards */
  .bottom-cards {{
    display: flex;
    gap: 14px;
    height: 310px;
  }}

  .card {{
    background: #f7faff;
    border: 1.5px solid #bce0fd;
    border-radius: 10px;
    padding: 12px 16px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}

  .card-board {{
    flex: 1.15;
  }}
  .card-led {{
    flex: 1.25;
    background: #f4fbf7;
    border-color: #c0ebd2;
  }}
  .card-api {{
    flex: 1.1;
    background: #f8f9fe;
    border-color: #d6def5;
  }}

  .card-title {{
    font-size: 15.5px;
    font-weight: 700;
    color: #014282;
    margin-bottom: 8px;
  }}

  /* Board Photo in Card */
  .board-container {{
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: center;
    background: #ffffff;
    border-radius: 8px;
    border: 1px solid #ddecfa;
    padding: 6px;
  }}
  .board-img {{
    max-width: 100%;
    max-height: 185px;
    object-fit: contain;
  }}
  .board-caption {{
    font-size: 11px;
    color: #475569;
    line-height: 1.35;
    margin-top: 8px;
  }}

  /* LED Details Table */
  .led-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 11.5px;
    margin-bottom: 10px;
  }}
  .led-table tr {{
    border-bottom: 1px solid #d5edd9;
  }}
  .led-table tr:last-child {{
    border-bottom: none;
  }}
  .led-table td {{
    padding: 7px 4px;
  }}
  .led-table td.col-key {{
    font-weight: 700;
    color: #1e3a8a;
    width: 42%;
  }}
  .led-table td.col-val {{
    color: #0f172a;
    font-weight: 500;
  }}
  .led-table td.col-val code {{
    background: #e2f2e5;
    padding: 1.5px 5px;
    border-radius: 3px;
    font-family: SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    font-size: 11px;
    color: #14532d;
    font-weight: 600;
  }}

  .tip-box {{
    background: #e8f5e9;
    border: 1.5px solid #a5d6a7;
    border-radius: 7px;
    padding: 8px 12px;
    display: flex;
    align-items: center;
    gap: 8px;
  }}
  .check-circle {{
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background: #2e7d32;
    color: #ffffff;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    font-weight: bold;
    flex-shrink: 0;
  }}
  .tip-text {{
    font-size: 11px;
    color: #1b5e20;
    font-weight: 600;
    line-height: 1.3;
  }}

  /* API Pills */
  .api-pills {{
    display: flex;
    flex-direction: column;
    gap: 8px;
    flex: 1;
    justify-content: center;
  }}
  .api-pill {{
    background: #ffffff;
    border: 1.5px solid #d4def7;
    border-radius: 7px;
    padding: 9px 12px;
  }}
  .api-fn {{
    font-family: SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    font-size: 12px;
    font-weight: 700;
    color: #014282;
  }}
  .api-desc {{
    font-size: 11px;
    color: #475569;
    margin-top: 2px;
  }}
</style>
</head>
<body>

<!-- Background subtle waves -->
<svg class="bg-waves" viewBox="0 0 1240 750" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M-50,200 C150,150 250,300 450,250 C650,200 750,350 950,300 C1150,250 1250,400 1350,350" stroke="#00A3E0" stroke-width="2" fill="none"/>
  <path d="M-50,240 C150,190 250,340 450,290 C650,240 750,390 950,340 C1150,290 1250,440 1350,390" stroke="#003B71" stroke-width="1.5" fill="none"/>
  <path d="M-50,280 C150,230 250,380 450,330 C650,280 750,430 950,380 C1150,330 1250,480 1350,430" stroke="#00A3E0" stroke-width="1" fill="none"/>
</svg>

<div class="main-card">

  <!-- Header -->
  <div class="header-bar">
    <div class="header-title">Blinky Application: Timing Pattern</div>
    <div class="header-subtitle">One complete 5-second cycle · Not to scale</div>
  </div>

  <!-- Top Timing Diagram -->
  <div class="timing-section">
    <div class="timing-diagram">
      <div class="pairs-row">

        <!-- 1st pair -->
        <div class="pair-group">
          <div class="pair-label">
            <span>1<sup>st</sup> pair</span>
            <svg class="curly-bracket" viewBox="0 0 86 10">
              <path d="M 2,8 Q 2,2 10,2 L 38,2 Q 43,2 43,0 Q 43,2 48,2 L 76,2 Q 84,2 84,8" fill="none" stroke="#014282" stroke-width="1.2"/>
            </svg>
          </div>
          <div class="pair-boxes">
            <div class="box box-on"><span class="state">ON</span><span class="time">350 ms</span></div>
            <div class="box box-off"><span class="state">OFF</span><span class="time">450 ms</span></div>
          </div>
        </div>

        <!-- 2nd pair -->
        <div class="pair-group">
          <div class="pair-label">
            <span>2<sup>nd</sup> pair</span>
            <svg class="curly-bracket" viewBox="0 0 86 10">
              <path d="M 2,8 Q 2,2 10,2 L 38,2 Q 43,2 43,0 Q 43,2 48,2 L 76,2 Q 84,2 84,8" fill="none" stroke="#014282" stroke-width="1.2"/>
            </svg>
          </div>
          <div class="pair-boxes">
            <div class="box box-on"><span class="state">ON</span><span class="time">350 ms</span></div>
            <div class="box box-off"><span class="state">OFF</span><span class="time">450 ms</span></div>
          </div>
        </div>

        <!-- 3rd pair -->
        <div class="pair-group">
          <div class="pair-label">
            <span>3<sup>rd</sup> pair</span>
            <svg class="curly-bracket" viewBox="0 0 86 10">
              <path d="M 2,8 Q 2,2 10,2 L 38,2 Q 43,2 43,0 Q 43,2 48,2 L 76,2 Q 84,2 84,8" fill="none" stroke="#014282" stroke-width="1.2"/>
            </svg>
          </div>
          <div class="pair-boxes">
            <div class="box box-on"><span class="state">ON</span><span class="time">350 ms</span></div>
            <div class="box box-off"><span class="state">OFF</span><span class="time">450 ms</span></div>
          </div>
        </div>

        <!-- 4th pair -->
        <div class="pair-group">
          <div class="pair-label">
            <span>4<sup>th</sup> pair</span>
            <svg class="curly-bracket" viewBox="0 0 86 10">
              <path d="M 2,8 Q 2,2 10,2 L 38,2 Q 43,2 43,0 Q 43,2 48,2 L 76,2 Q 84,2 84,8" fill="none" stroke="#014282" stroke-width="1.2"/>
            </svg>
          </div>
          <div class="pair-boxes">
            <div class="box box-on"><span class="state">ON</span><span class="time">350 ms</span></div>
            <div class="box box-off"><span class="state">OFF</span><span class="time">450 ms</span></div>
          </div>
        </div>

        <!-- 5th pair -->
        <div class="pair-group">
          <div class="pair-label">
            <span>5<sup>th</sup> pair</span>
            <svg class="curly-bracket" viewBox="0 0 86 10">
              <path d="M 2,8 Q 2,2 10,2 L 38,2 Q 43,2 43,0 Q 43,2 48,2 L 76,2 Q 84,2 84,8" fill="none" stroke="#014282" stroke-width="1.2"/>
            </svg>
          </div>
          <div class="pair-boxes">
            <div class="box box-on"><span class="state">ON</span><span class="time">350 ms</span></div>
            <div class="box box-off"><span class="state">OFF</span><span class="time">450 ms</span></div>
          </div>
        </div>

        <!-- Additional Pause -->
        <div class="pair-group">
          <div class="pair-label" style="opacity: 0;">
            <span>Pause</span>
            <svg class="curly-bracket" viewBox="0 0 86 10"></svg>
          </div>
          <div class="box box-pause">
            <span class="state">LED OFF</span>
            <span class="time">Additional 1,000 ms</span>
          </div>
        </div>

      </div>

      <!-- Dimension lines -->
      <div class="dim-line-container">
        <div class="dim-row-1">
          <div class="dim-arrow-5x">
            <div class="arrow-line arrow-left"></div>
            <span>Repeat the ON/OFF pair 5 times = 4,000 ms</span>
            <div class="arrow-line arrow-right"></div>
          </div>
          <div class="dim-arrow-pause">
            <div class="arrow-line arrow-left"></div>
            <span>1,000 ms</span>
            <div class="arrow-line arrow-right"></div>
          </div>
        </div>

        <div class="dim-row-total">
          <div class="arrow-line arrow-left"></div>
          <span>5,000 ms per cycle</span>
          <div class="arrow-line arrow-right"></div>
        </div>
      </div>
    </div>

    <!-- Legend Box -->
    <div class="legend-box">
      <div class="legend-item">
        <div class="legend-swatch swatch-on"></div>
        <div class="legend-text">
          <strong>LED ON</strong>
          <span>(350 ms)</span>
        </div>
      </div>
      <div class="legend-item">
        <div class="legend-swatch swatch-off"></div>
        <div class="legend-text">
          <strong>LED OFF</strong>
          <span>(450 ms)</span>
        </div>
      </div>
      <div class="legend-item">
        <div class="legend-swatch swatch-pause"></div>
        <div class="legend-text">
          <strong>Additional OFF</strong>
          <span>(1,000 ms)</span>
        </div>
      </div>
    </div>
  </div>

  <!-- Bottom Cards Row -->
  <div class="bottom-cards">

    <!-- Card 1: Board Photo -->
    <div class="card card-board">
      <div class="card-title">PIC32CM GC00 Curiosity Pro</div>
      <div class="board-container">
        <img class="board-img" src="file://{board_img_path}" alt="PIC32CM GC00 Curiosity Pro Board">
      </div>
      <div class="board-caption">
        The LED is connected to the board's user LED pin as defined in the Devicetree.
      </div>
    </div>

    <!-- Card 2: Board LED Details -->
    <div class="card card-led">
      <div class="card-title">Board LED Details</div>
      <table class="led-table">
        <tr>
          <td class="col-key">Devicetree node</td>
          <td class="col-val"><code>&led0</code> (DT_ALIAS)</td>
        </tr>
        <tr>
          <td class="col-key">GPIO controller</td>
          <td class="col-val"><code>PORTA</code> (gpio_mchp_port_g1)</td>
        </tr>
        <tr>
          <td class="col-key">Pin</td>
          <td class="col-val"><code>PA20</code> (Pin 20 on Port A)</td>
        </tr>
        <tr>
          <td class="col-key">Active polarity</td>
          <td class="col-val"><code>Active Low</code> (0V = ON, 3.3V = OFF)</td>
        </tr>
      </table>
      <div class="tip-box">
        <div class="check-circle">&#10003;</div>
        <div class="tip-text">
          Use the board's actual Devicetree LED specification and active polarity.
        </div>
      </div>
    </div>

    <!-- Card 3: Zephyr API -->
    <div class="card card-api">
      <div class="card-title">Zephyr API (used in code)</div>
      <div class="api-pills">
        <div class="api-pill">
          <div class="api-fn">gpio_pin_configure_dt()</div>
          <div class="api-desc">– configure the LED GPIO.</div>
        </div>
        <div class="api-pill">
          <div class="api-fn">gpio_pin_set_dt()</div>
          <div class="api-desc">– set the LED state.</div>
        </div>
        <div class="api-pill">
          <div class="api-fn">k_msleep()</div>
          <div class="api-desc">– wait for the required interval.</div>
        </div>
      </div>
    </div>

  </div>

</div>
</body>
</html>
"""

# Template 2: Comprehensive version that includes the Serial Telemetry Output
html_content_output = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  @page {{
    size: 1300px 840px;
    margin: 0;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    background: #f4f8fc;
    width: 1300px;
    height: 840px;
    padding: 16px;
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
    overflow: hidden;
  }}

  .main-card {{
    position: relative;
    z-index: 1;
    width: 1268px;
    height: 808px;
    background: #ffffff;
    border: 1.5px solid #b8daff;
    border-radius: 14px;
    padding: 16px 20px;
    box-shadow: 0 10px 30px rgba(0, 59, 113, 0.08);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}

  .header-bar {{
    background: #014282;
    border-radius: 7px;
    padding: 10px 22px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    color: #ffffff;
  }}
  .header-title {{
    font-size: 20px;
    font-weight: 700;
    white-space: nowrap;
  }}
  .header-subtitle {{
    font-size: 13.5px;
    color: #d4e8fc;
    white-space: nowrap;
  }}

  /* Top Section: Timing Pattern */
  .timing-section {{
    background: #edf6fd;
    border: 1.5px solid #bce0fd;
    border-radius: 10px;
    padding: 12px 18px 10px 18px;
    display: flex;
    gap: 16px;
  }}

  .timing-diagram {{
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}

  .pairs-row {{
    display: flex;
    align-items: flex-end;
    gap: 10px;
  }}
  .pair-group {{
    display: flex;
    flex-direction: column;
    align-items: center;
  }}
  .pair-label {{
    font-size: 11.5px;
    font-weight: 600;
    color: #014282;
    margin-bottom: 2px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }}
  .curly-bracket {{
    width: 86px;
    height: 9px;
    margin-bottom: 2px;
  }}
  .pair-boxes {{
    display: flex;
    gap: 2px;
  }}
  .box {{
    border-radius: 5px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
  }}
  .box-on {{
    width: 45px;
    height: 52px;
    background: #a9e8b7;
    border: 1.5px solid #66bb6a;
  }}
  .box-on .state {{ font-size: 12px; font-weight: 700; color: #0f5132; }}
  .box-on .time {{ font-size: 9.5px; color: #1b5e20; }}

  .box-off {{
    width: 45px;
    height: 52px;
    background: #bce3fb;
    border: 1.5px solid #4fc3f7;
  }}
  .box-off .state {{ font-size: 12px; font-weight: 700; color: #084298; }}
  .box-off .time {{ font-size: 9.5px; color: #0d47a1; }}

  .box-pause {{
    width: 130px;
    height: 52px;
    background: #cfd8dc;
    border: 1.5px solid #90a4ae;
    margin-left: 2px;
  }}
  .box-pause .state {{ font-size: 12px; font-weight: 700; color: #263238; }}
  .box-pause .time {{ font-size: 9.5px; color: #37474f; }}

  /* Dimension lines */
  .dim-line-container {{
    margin-top: 8px;
    display: flex;
    flex-direction: column;
    gap: 4px;
  }}
  .dim-row-1 {{
    display: flex;
    align-items: center;
    font-size: 10.5px;
    color: #014282;
    font-weight: 600;
  }}
  .dim-arrow-5x {{
    width: 504px;
    display: flex;
    align-items: center;
    gap: 6px;
  }}
  .dim-arrow-pause {{
    width: 130px;
    margin-left: 12px;
    display: flex;
    align-items: center;
    gap: 4px;
    justify-content: center;
  }}
  .dim-row-total {{
    display: flex;
    align-items: center;
    font-size: 11.5px;
    color: #014282;
    font-weight: 700;
    width: 646px;
    gap: 8px;
  }}
  .arrow-line {{
    flex: 1;
    height: 1px;
    background: #014282;
    position: relative;
  }}
  .arrow-left::before {{
    content: '';
    position: absolute;
    left: 0;
    top: -3px;
    width: 0;
    height: 0;
    border-top: 3px solid transparent;
    border-bottom: 3px solid transparent;
    border-right: 5px solid #014282;
  }}
  .arrow-right::after {{
    content: '';
    position: absolute;
    right: 0;
    top: -3px;
    width: 0;
    height: 0;
    border-top: 3px solid transparent;
    border-bottom: 3px solid transparent;
    border-left: 5px solid #014282;
  }}

  /* Legend */
  .legend-box {{
    width: 168px;
    background: #ffffff;
    border: 1.5px solid #cce4fc;
    border-radius: 8px;
    padding: 8px 12px;
    display: flex;
    flex-direction: column;
    justify-content: space-around;
  }}
  .legend-item {{ display: flex; align-items: center; gap: 8px; }}
  .legend-swatch {{ width: 20px; height: 20px; border-radius: 4px; flex-shrink: 0; }}
  .swatch-on {{ background: #a9e8b7; border: 1.5px solid #66bb6a; }}
  .swatch-off {{ background: #bce3fb; border: 1.5px solid #4fc3f7; }}
  .swatch-pause {{ background: #cfd8dc; border: 1.5px solid #90a4ae; }}
  .legend-text {{ font-size: 10.5px; }}
  .legend-text strong {{ display: block; color: #0f172a; }}
  .legend-text span {{ color: #64748b; font-size: 9.5px; }}

  /* Bottom 4-Column Layout */
  .bottom-cards {{
    display: flex;
    gap: 12px;
    height: 470px;
  }}
  .card {{
    background: #f7faff;
    border: 1.5px solid #bce0fd;
    border-radius: 10px;
    padding: 12px 14px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}
  .card-board {{ flex: 1; }}
  .card-led {{ flex: 1.1; background: #f4fbf7; border-color: #c0ebd2; }}
  .card-output {{ flex: 1.25; background: #0f172a; border-color: #334155; color: #f8fafc; }}
  .card-title {{
    font-size: 14.5px;
    font-weight: 700;
    color: #014282;
    margin-bottom: 6px;
  }}
  .card-output .card-title {{
    color: #38bdf8;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}
  .baud-badge {{
    background: #1e293b;
    border: 1px solid #475569;
    color: #94a3b8;
    font-size: 10px;
    padding: 2px 6px;
    border-radius: 4px;
    font-family: monospace;
  }}

  .board-container {{
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: center;
    background: #ffffff;
    border-radius: 8px;
    border: 1px solid #ddecfa;
    padding: 6px;
  }}
  .board-img {{
    max-width: 100%;
    max-height: 280px;
    object-fit: contain;
  }}
  .board-caption {{
    font-size: 10.5px;
    color: #475569;
    margin-top: 6px;
  }}

  .led-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 11px;
    margin-bottom: 8px;
  }}
  .led-table tr {{ border-bottom: 1px solid #d5edd9; }}
  .led-table td {{ padding: 6px 3px; }}
  .led-table td.col-key {{ font-weight: 700; color: #1e3a8a; }}
  .led-table td.col-val code {{
    background: #e2f2e5;
    padding: 1px 4px;
    border-radius: 3px;
    font-family: monospace;
    font-size: 10.5px;
    color: #14532d;
    font-weight: 600;
  }}

  .tip-box {{
    background: #e8f5e9;
    border: 1.5px solid #a5d6a7;
    border-radius: 6px;
    padding: 6px 10px;
    display: flex;
    align-items: center;
    gap: 6px;
  }}
  .check-circle {{
    width: 18px; height: 18px; border-radius: 50%;
    background: #2e7d32; color: #fff;
    display: flex; align-items: center; justify-content: center;
    font-size: 11px; font-weight: bold; flex-shrink: 0;
  }}
  .tip-text {{ font-size: 10px; color: #1b5e20; font-weight: 600; }}

  /* Terminal Log Box */
  .terminal-box {{
    background: #020617;
    border: 1px solid #1e293b;
    border-radius: 7px;
    padding: 10px 12px;
    font-family: SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    font-size: 10.5px;
    line-height: 1.45;
    color: #cbd5e1;
    flex: 1;
    overflow: hidden;
  }}
  .term-green {{ color: #4ade80; font-weight: 600; }}
  .term-cyan {{ color: #38bdf8; font-weight: 600; }}
  .term-dim {{ color: #64748b; }}
  .term-gold {{ color: #facc15; font-weight: 600; }}
</style>
</head>
<body>
<div class="main-card">

  <div class="header-bar">
    <div class="header-title">Blinky Application: Timing Pattern & Serial Telemetry</div>
    <div class="header-subtitle">One complete 5-second cycle · Authentic Hardware Specifications</div>
  </div>

  <div class="timing-section">
    <div class="timing-diagram">
      <div class="pairs-row">
        <div class="pair-group">
          <div class="pair-label"><span>1<sup>st</sup> pair</span><svg class="curly-bracket" viewBox="0 0 86 10"><path d="M 2,8 Q 2,2 10,2 L 38,2 Q 43,2 43,0 Q 43,2 48,2 L 76,2 Q 84,2 84,8" fill="none" stroke="#014282" stroke-width="1.2"/></svg></div>
          <div class="pair-boxes"><div class="box box-on"><span class="state">ON</span><span class="time">350 ms</span></div><div class="box box-off"><span class="state">OFF</span><span class="time">450 ms</span></div></div>
        </div>
        <div class="pair-group">
          <div class="pair-label"><span>2<sup>nd</sup> pair</span><svg class="curly-bracket" viewBox="0 0 86 10"><path d="M 2,8 Q 2,2 10,2 L 38,2 Q 43,2 43,0 Q 43,2 48,2 L 76,2 Q 84,2 84,8" fill="none" stroke="#014282" stroke-width="1.2"/></svg></div>
          <div class="pair-boxes"><div class="box box-on"><span class="state">ON</span><span class="time">350 ms</span></div><div class="box box-off"><span class="state">OFF</span><span class="time">450 ms</span></div></div>
        </div>
        <div class="pair-group">
          <div class="pair-label"><span>3<sup>rd</sup> pair</span><svg class="curly-bracket" viewBox="0 0 86 10"><path d="M 2,8 Q 2,2 10,2 L 38,2 Q 43,2 43,0 Q 43,2 48,2 L 76,2 Q 84,2 84,8" fill="none" stroke="#014282" stroke-width="1.2"/></svg></div>
          <div class="pair-boxes"><div class="box box-on"><span class="state">ON</span><span class="time">350 ms</span></div><div class="box box-off"><span class="state">OFF</span><span class="time">450 ms</span></div></div>
        </div>
        <div class="pair-group">
          <div class="pair-label"><span>4<sup>th</sup> pair</span><svg class="curly-bracket" viewBox="0 0 86 10"><path d="M 2,8 Q 2,2 10,2 L 38,2 Q 43,2 43,0 Q 43,2 48,2 L 76,2 Q 84,2 84,8" fill="none" stroke="#014282" stroke-width="1.2"/></svg></div>
          <div class="pair-boxes"><div class="box box-on"><span class="state">ON</span><span class="time">350 ms</span></div><div class="box box-off"><span class="state">OFF</span><span class="time">450 ms</span></div></div>
        </div>
        <div class="pair-group">
          <div class="pair-label"><span>5<sup>th</sup> pair</span><svg class="curly-bracket" viewBox="0 0 86 10"><path d="M 2,8 Q 2,2 10,2 L 38,2 Q 43,2 43,0 Q 43,2 48,2 L 76,2 Q 84,2 84,8" fill="none" stroke="#014282" stroke-width="1.2"/></svg></div>
          <div class="pair-boxes"><div class="box box-on"><span class="state">ON</span><span class="time">350 ms</span></div><div class="box box-off"><span class="state">OFF</span><span class="time">450 ms</span></div></div>
        </div>
        <div class="pair-group">
          <div class="pair-label" style="opacity: 0;"><span>Pause</span></div>
          <div class="box box-pause"><span class="state">LED OFF</span><span class="time">Additional 1,000 ms</span></div>
        </div>
      </div>

      <div class="dim-line-container">
        <div class="dim-row-1">
          <div class="dim-arrow-5x"><div class="arrow-line arrow-left"></div><span>Repeat the ON/OFF pair 5 times = 4,000 ms</span><div class="arrow-line arrow-right"></div></div>
          <div class="dim-arrow-pause"><div class="arrow-line arrow-left"></div><span>1,000 ms</span><div class="arrow-line arrow-right"></div></div>
        </div>
        <div class="dim-row-total"><div class="arrow-line arrow-left"></div><span>5,000 ms per cycle</span><div class="arrow-line arrow-right"></div></div>
      </div>
    </div>

    <div class="legend-box">
      <div class="legend-item"><div class="legend-swatch swatch-on"></div><div class="legend-text"><strong>LED ON</strong><span>(350 ms)</span></div></div>
      <div class="legend-item"><div class="legend-swatch swatch-off"></div><div class="legend-text"><strong>LED OFF</strong><span>(450 ms)</span></div></div>
      <div class="legend-item"><div class="legend-swatch swatch-pause"></div><div class="legend-text"><strong>Additional OFF</strong><span>(1,000 ms)</span></div></div>
    </div>
  </div>

  <div class="bottom-cards">
    <!-- Card 1: Board Photo -->
    <div class="card card-board">
      <div class="card-title">PIC32CM GC00 Curiosity Pro</div>
      <div class="board-container">
        <img class="board-img" src="file://{board_img_path}" alt="PIC32CM GC00 Curiosity Pro Board">
      </div>
      <div class="board-caption">Microchip SAM D21 / PIC32CM ARM Cortex-M23 Evaluation Platform</div>
    </div>

    <!-- Card 2: Board Details & APIs -->
    <div class="card card-led">
      <div class="card-title">Hardware Devicetree Mapping</div>
      <table class="led-table">
        <tr><td class="col-key">Devicetree node</td><td class="col-val"><code>&led0</code> (DT_ALIAS)</td></tr>
        <tr><td class="col-key">GPIO controller</td><td class="col-val"><code>PORTA</code></td></tr>
        <tr><td class="col-key">Pin</td><td class="col-val"><code>PA20</code> (User LED0)</td></tr>
        <tr><td class="col-key">Active polarity</td><td class="col-val"><code>Active Low</code> (0V = ON)</td></tr>
        <tr><td class="col-key">Zephyr API</td><td class="col-val"><code>gpio_pin_set_dt()</code></td></tr>
        <tr><td class="col-key">Kernel Sleep</td><td class="col-val"><code>k_msleep()</code></td></tr>
      </table>
      <div class="tip-box">
        <div class="check-circle">&#10003;</div>
        <div class="tip-text">Active-Low: Driven LOW to sink current & illuminate LED.</div>
      </div>
    </div>

    <!-- Card 3: Serial Console Output -->
    <div class="card card-output">
      <div class="card-title">
        <span>UART Serial Telemetry</span>
        <span class="baud-badge">115200 8N1</span>
      </div>
      <div class="terminal-box">
        <div class="term-dim">*** Booting Zephyr OS build v3.7.0 ***</div>
        <div>Iteration 1/5 - LED state: <span class="term-green">ON</span> (350 ms ON)</div>
        <div>Iteration 1/5 - LED state: <span class="term-cyan">OFF</span> (450 ms OFF)</div>
        <div>Iteration 2/5 - LED state: <span class="term-green">ON</span> (350 ms ON)</div>
        <div>Iteration 2/5 - LED state: <span class="term-cyan">OFF</span> (450 ms OFF)</div>
        <div>Iteration 3/5 - LED state: <span class="term-green">ON</span> (350 ms ON)</div>
        <div>Iteration 3/5 - LED state: <span class="term-cyan">OFF</span> (450 ms OFF)</div>
        <div>Iteration 4/5 - LED state: <span class="term-green">ON</span> (350 ms ON)</div>
        <div>Iteration 4/5 - LED state: <span class="term-cyan">OFF</span> (450 ms OFF)</div>
        <div>Iteration 5/5 - LED state: <span class="term-green">ON</span> (350 ms ON)</div>
        <div>Iteration 5/5 - LED state: <span class="term-cyan">OFF</span> (450 ms OFF)</div>
        <div><span class="term-gold">Pause</span> - LED state: <span class="term-cyan">OFF</span> (1000 ms Pause)</div>
      </div>
    </div>
  </div>

</div>
</body>
</html>
"""

# Render both images
for name, html in [
    ("pic32cm_blinky_timing_pattern", html_content_pattern),
    ("pic32cm_blinky_timing_and_output", html_content_output)
]:
    html_file = f"/tmp/{name}.html"
    pdf_file = f"/tmp/{name}.pdf"
    with open(html_file, "w") as f:
        f.write(html)
    print(f"Rendering {name} via WeasyPrint...")
    weasyprint.HTML(html_file).write_pdf(pdf_file)
    subprocess.run(["pdftoppm", "-png", "-r", "150", pdf_file, f"/tmp/{name}_ppm"], check=True)
    out_png = f"/home/sujan/zephyrproject/pic32cm_gc00_blinky/assets/{name}.png"
    os.system(f"cp /tmp/{name}_ppm-1.png {out_png}")
    os.system(f"cp {out_png} /home/sujan/zephyrproject/{name}.png")
    print(f"Created: {out_png}")

print("Both graphic slides created successfully!")
