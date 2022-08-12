import numpy as np
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.express.colors import sample_colorscale

######################
### Importar Datos ###
######################

csv_path = "DataframesClima/"

precipitacion_df = pd.read_csv(csv_path+"precipitacion_anual.csv")
temperaturas_min_df = pd.read_csv(csv_path+"temperaturas_min.csv")
temperaturas_max_df = pd.read_csv(csv_path+"temperaturas_max.csv")
temperaturas_mean_df = pd.read_csv(csv_path+"temperaturas_mean.csv")


precipitacion=precipitacion_df.melt(id_vars=["ENTIDAD", "año"], 
        var_name="Mes", 
        value_name="Precipitación")

temperaturas_min=temperaturas_min_df.melt(id_vars=["ENTIDAD", "año"], 
        var_name="Mes", 
        value_name="Temperatura Mínima")

temperaturas_mean=temperaturas_mean_df.melt(id_vars=["ENTIDAD", "año"], 
        var_name="Mes", 
        value_name="Temperatura Promedio")

temperaturas_max=temperaturas_max_df.melt(id_vars=["ENTIDAD", "año"], 
        var_name="Mes", 
        value_name="Temperatura Máxima")

variables_climatologicas=pd.merge(pd.merge(precipitacion, temperaturas_min, on=["ENTIDAD","año","Mes"]), pd.merge(temperaturas_mean, temperaturas_max, on=["ENTIDAD","año","Mes"]), on=["ENTIDAD","año","Mes"])


def data_frame(Variable, Entidad):
	if Variable=='Precipitación':
		df=precipitacion_df.loc[precipitacion_df['ENTIDAD']==Entidad,~precipitacion_df.columns.isin(['ENTIDAD','ANUAL'])].set_index('año').T
	elif Variable=='Temperatura Mínima':
		df=temperaturas_min_df.loc[temperaturas_min_df['ENTIDAD']==Entidad,~temperaturas_min_df.columns.isin(['ENTIDAD','ANUAL'])].set_index('año').T
	elif Variable=='Temperatura Promedio':
		df=temperaturas_mean_df.loc[temperaturas_mean_df['ENTIDAD']==Entidad,~temperaturas_mean_df.columns.isin(['ENTIDAD','ANUAL'])].set_index('año').T
	elif Variable=='Temperatura Máxima':
		df=temperaturas_max_df.loc[temperaturas_max_df['ENTIDAD']==Entidad,~temperaturas_max_df.columns.isin(['ENTIDAD','ANUAL'])].set_index('año').T
	df.index.name='Mes'
	año_prom = df.mean(axis=0, numeric_only=True).to_frame().rename(columns={0:'Precipitación Promedio'})
	mes_prom = df.mean(axis=1, numeric_only=True).to_frame().rename(columns={0:'Precipitación Promedio'})
	return df, año_prom, mes_prom




################
### Gráficas ###
################

def heat_map(Variable, Entidad):
	df, año_prom, mes_prom = data_frame(Variable, Entidad)
	fig_1=go.Figure(go.Heatmap(x=df.columns.values, y=df.index.values, z=df.values,
                                   coloraxis="coloraxis",
                                   name='')
              	        )
	if Variable=='Precipitación':
    		fig_1.update_layout(coloraxis=dict(colorscale='Blues'), coloraxis_colorbar=dict(title='mm/m<sup>2<sup>',
				  bordercolor='white', borderwidth=1, outlinecolor='white', outlinewidth=1)
				  )
	else:
    		fig_1.update_layout(template='plotly_white',
				  coloraxis=dict(colorscale='hot'), coloraxis_colorbar=dict(title='°C',
				  bordercolor='white', borderwidth=1, outlinecolor='white', outlinewidth=1)
				  )
	fig_1.update_layout(plot_bgcolor='rgba(0,0,0,0)', margin_b=0, margin_l=0, margin_r=0, margin_t=40, height=350)
	fig_1.update_xaxes(title_text='Año', tickangle=60, dtick=1, gridcolor='black')
	fig_1.update_yaxes(title_text='Mes', gridcolor='black')
	fig_1.update_traces(hovertemplate='%{y} %{x}<br><br><b>'+Variable+':<br>%{z}</b>')
	st.plotly_chart(fig_1, use_container_width=True)

def Prom_Mes(Variable, Entidad):
	df, mes_prom, año_prom = data_frame(Variable, Entidad)
	fig_2=go.Figure(go.Bar(x=mes_prom.index, y=mes_prom['Precipitación Promedio'],
                    	       marker=dict(color=mes_prom['Precipitación Promedio'], coloraxis="coloraxis"),
                    	       showlegend=False, name='')
              	        )
	if Variable=='Precipitación':
    		fig_2.update_layout(template='plotly_dark',
				  coloraxis=dict(colorscale='Blues'), coloraxis_colorbar=dict(title='mm/m<sup>2<sup>',
				  bordercolor='white', borderwidth=1, outlinecolor='white', outlinewidth=1))
	else:
    		fig_2.update_layout(template='plotly_white',
				  coloraxis=dict(colorscale='hot'), coloraxis_colorbar=dict(title='°C',
				  bordercolor='white', borderwidth=1, outlinecolor='white', outlinewidth=1)
				  )
	if Variable=='Precipitación':
		unidad=' [mm/m<sup>2</sup>]'
	else:
		unidad=' [°C]'
	fig_2.update_layout(barmode='group', bargap=0, plot_bgcolor='rgba(0,0,0,0)', coloraxis_showscale=False,
			    margin_b=0, margin_l=0, margin_r=0, margin_t=40, height=250)
	fig_2.update_coloraxes(cmin=df.min().min(), cmax=df.max().max())
	fig_2.update_xaxes(title_text='Mes', tickangle=60, dtick=1)
	fig_2.update_yaxes(title_text='Promedio Mensual'+unidad)
	fig_2.update_traces(hovertemplate='%{x}<br><br><b>'+Variable+':<br>%{y:.1f}</b>')
	st.plotly_chart(fig_2, use_container_width=True)



def Prom_Año(Variable, Entidad):
	df, mes_prom, año_prom = data_frame(Variable, Entidad)
	fig_3=go.Figure(go.Bar(x=año_prom.index, y=año_prom['Precipitación Promedio'],
                    	       marker=dict(color=año_prom['Precipitación Promedio'], coloraxis="coloraxis"),
                    	       showlegend=False, name='')
              	        )
	if Variable=='Precipitación':
    		fig_3.update_layout(template='plotly_dark',
				  coloraxis=dict(colorscale='Blues'), coloraxis_colorbar=dict(title='mm/m<sup>2<sup>',
				  bordercolor='white', borderwidth=1, outlinecolor='white', outlinewidth=1)
				  )
	else:
    		fig_3.update_layout(template='plotly_white',
				  coloraxis=dict(colorscale='hot'), coloraxis_colorbar=dict(title='°C',
				  bordercolor='white', borderwidth=1, outlinecolor='white', outlinewidth=1)
				  )
	if Variable=='Precipitación':
		unidad=' [mm/m<sup>2</sup>]'
	else:
		unidad=' [°C]'
	fig_3.update_layout(barmode='group', bargap=0, plot_bgcolor='rgba(0,0,0,0)', coloraxis_showscale=False,
			    margin_b=0, margin_l=0, margin_r=0, margin_t=40, height=250)
	fig_3.update_coloraxes(cmin=df.min().min(), cmax=df.max().max())
	fig_3.update_yaxes(title_text='Promedio Anual'+unidad)
	fig_3.update_xaxes(title_text='Año', tickangle=60, dtick=1)
	fig_3.update_traces(hovertemplate='%{x}<br><br><b>'+Variable+':<br>%{y:.1f}</b>')
	st.plotly_chart(fig_3, use_container_width=True)



def Historico(Variable, Entidad):
	df, mes_prom, año_prom = data_frame(Variable, Entidad)
	df_H = variables_climatologicas[(variables_climatologicas['Mes']!='ANUAL') & (variables_climatologicas['ENTIDAD']==Entidad)]
	df_U=df_H.set_index(['año'])
	minimo=df.min().min()
	maximo=df.max().max()
	if Variable=='Precipitación':
		escala='Blues'
	else:
		escala='Hot'
	fig_4 = go.Figure()
	for i in df_U.index.unique():
		c=(df_U.loc[i][Variable].median()-minimo)/(maximo-minimo)
		fig_4.add_trace(go.Box(y=df_U.loc[i][Variable], name=i, showlegend=False,
				#boxmean=True,
				marker_color=sample_colorscale(escala,c)[0])
				)
	if Variable=='Precipitación':
		unidad=' [mm/m<sup>2</sup>]'
	else:
		unidad=' [°C]'
	fig_4.update_layout(plot_bgcolor='rgba(0,0,0,0)', margin_b=0, margin_l=0, margin_r=0, margin_t=40, height=250)
	fig_4.update_yaxes(title_text=Variable+unidad)
	fig_4.update_xaxes(title_text='Año', tickangle=60, dtick=1)
	st.plotly_chart(fig_4, use_container_width=True)



def Banda_error_cont(Variable, Entidad):
	df_5=variables_climatologicas[(variables_climatologicas['Mes']!='ANUAL') & (variables_climatologicas['ENTIDAD']==Entidad)]
	y=df_5.groupby(['año']).mean()
	desv=df_5.groupby(['año']).std()
	y_max=y+desv
	y_min=np.maximum(y-desv, 0)
	if Variable=='Precipitación':
		c_lin=sample_colorscale('Blues',0.7)[0]
		c_fill='rgba(182,212,233,0.7)'	#0.3
		#c_fill='rgba(148,196,223,0.7)'	#0.4
		unidad='mm/m<sup>2<sup>'
	else:
		c_lin=sample_colorscale('Hot',0.6)[0]
		#c_fill='rgba(207,0,0,0.7)'	#0.3
		c_fill='rgba(235,42,0,0.7)'	#0.4
		unidad='°C'
	fig_5=go.Figure()
	fig_5.add_trace(go.Scatter(x=y.index, y=y_max[Variable], name='Media'+'+σ',
			mode='lines', line=dict(width=0), line_color=c_lin, showlegend=False))
	fig_5.add_trace(go.Scatter(x=y.index, y=y_min[Variable], name='Media'+'-σ',
			mode='lines', line=dict(width=0), line_color=c_lin, showlegend=False,
			fill='tonexty', fillcolor=c_fill))
	fig_5.add_trace(go.Scatter(x=y.index, y=y[Variable], name='Media',
			mode='lines', line_color=c_lin, showlegend=False))
	fig_5.update_layout(plot_bgcolor='rgba(0,0,0,0)', hovermode='x',
			    margin_b=0, margin_l=0, margin_r=0, margin_t=40, height=250)
	fig_5.update_yaxes(title_text=unidad)
	fig_5.update_xaxes(title_text='Año', tickangle=60, dtick=1, showgrid=False)
	st.plotly_chart(fig_5, use_container_width=True)





###############
### Sidebar ###
###############

st.set_page_config(layout='wide')









col1_1, col2_1, col3_1, col4_1 = st.columns([1,2,6,1])
with col2_1:
	st.write('')
	st.write('')
	st.write('')
	st.write('')
	Variable = st.radio('Variable Climatológica', ('Precipitación','Temperatura Mínima','Temperatura Promedio','Temperatura Máxima'), key='Temperatura Promedio')
	Entidad = st.selectbox('Entidad Federativa', tuple(precipitacion_df['ENTIDAD'].unique()), key='NACIONAL')
with col3_1:
	heat_map(Variable, Entidad)

col1_2, col2_2, col3_2, col4_2 = st.columns([1,4,4,1])
with col2_2:
	Prom_Mes(Variable, Entidad)
	Historico(Variable, Entidad)
with col3_2:
	Prom_Año(Variable, Entidad)
	Banda_error_cont(Variable, Entidad)