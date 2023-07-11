def HTML():
    html = """
    <div class="page page-with-bg">
        <br>
        </div>
        
        <div class="page-with-text">
        <div id="head">
            {date}
        </div>
        <div class="parent">
            <div class="Subtitle" id="sub1">Portfolio Overview</div>
            <div class="chart-container">
            <figure>
                <img src="graphs/donut.png" height="100%">
            </figure>
            <div class="chart-legend" id="allocation-legend">Your portfolio is valued at {portfolio_value}$ and contains mainly {important_stocks} </div>
            </div>
            <div class="paragraph" id="par1">{portfolio_overview}</div>
        </div>
        <div class="page-break"></div>
        
        <div class= "page-with-text" style="padding-top: 30px">

        <div class="parent">
            <div class="Subtitle" id="sib2">Performance evaluation</div>
            <div>
            <figure>
                <img src="graphs/benchmark.png" height="100%">
            </figure>
            <div class="chart-legend">{performance_vsSP500}</div>
            </div>
            <div class="paragraph" id="par4">{historical_performance}</div>
            </div>
        </div>
        </div>
        
        <div class="page-break"></div>
        
        <div class= "page-with-text" style="padding-top: 30px">

        <div class="parent">
            <div class="Subtitle" id="sib3">Risk exposure and Volatility</div>
            <div>
            <figure>
            <img src="graphs/beta.png">
            </figure>
            <div class="chart-legend">{beta_legend}</div>
            </div>
            <div class="paragraph" id="par5">{risk_exposure}</div>
        </div>
        </div>
        
        <div class="page-break"></div>
        
        <div class="page-with-text" style="padding-top: 30px">
        
        

        <div class="parent">
            <div class="Subtitle">
            Economic events
            </div>
            <div class="paragraph" id="par5" style="white-space: pre-line">Below is a detailed calendar highlighting both past and upcoming economic events that are expected to have a significant impact on your investment portfolio.</div>
            <section>
            <div class="events">
                <ul class="timeline" id="timeline">
                    <li class="today"><h3>Past Events</h3></li>
                    {previous_events}
                    <li class="today"><h3>Upcomming Events</h3></li>
                    {upcomming_events}
                </ul>
            </div>
            </section>
        </div>
        </div>
    """
    return html