<?php
/**
 * This class adds styling (color) options to the WordPress
 * Theme Customizer and outputs the needed CSS to the header
 * 
 * @link http://codex.wordpress.org/Theme_Customization_API
 * @package WordPress
 * @subpackage Fabulous WPExplorer Theme
 * @since Fabulous 1.0
 */

class WPEX_Theme_Customizer_Styling {

	/**
	* This hooks into 'customize_register' (available as of WP 3.4) and allows
	* you to add new sections and controls to the Theme Customize screen.
	*
	* @see add_action('register',$func)
	* @param \WP_Customize_Manager $wp_customize
	* @since Fabulous 1.0
	*/
	public static function register ( $wp_customize ) {

			// Theme Design Section
			$wp_customize->add_section( 'wpex_styling' , array(
				'title'		=> __( 'Styling', 'wpex' ),
				'priority'	=> 999,
			) );

			// Get Color Options
			$color_options = self::wpex_color_options();

			// Loop through color options and add a theme customizer setting for it
			$count='2';
			foreach( $color_options as $option ) {
				$count++;
				$default = isset($option['default']) ? $option['default'] : '';
				$type = isset($option['type']) ? $option['type'] : '';
				$wp_customize->add_setting( 'wpex_'. $option['id'] .'', array(
					'type'		=> 'theme_mod',
					'default'	=> $default,
					'transport'	=> 'refresh',
				) );
				if ( 'text' == $type ) {
					$wp_customize->add_control( 'wpex_'. $option['id'] .'', array(
						'label'		=> $option['label'],
						'section'	=> 'wpex_styling',
						'settings'	=> 'wpex_'. $option['id'] .'',
						'priority'	=> $count,
						'type'		=> 'text',
					) );
				} else {
					$wp_customize->add_control( new WP_Customize_Color_Control( $wp_customize, 'wpex_'. $option['id'] .'', array(
						'label'		=> $option['label'],
						'section'	=> 'wpex_styling',
						'settings'	=> 'wpex_'. $option['id'] .'',
						'priority'	=> $count,
					) ) );
				}
			} // End foreach

	} // End register


	/**
	* This will output the custom styling settings to the live theme's WP head.
	* Used by hook: 'wp_head'
	* 
	* @see add_action('wp_head',$func)
	* @since Fabulous 1.0
	*/
	public static function header_output() {
		$color_options = self::wpex_color_options();
		$css ='';
		foreach( $color_options as $option ) {
			$theme_mod = get_theme_mod('wpex_'. $option['id'] .'');
			if ( '' != $theme_mod ) {
				if ( !empty($option['media_query']) ) {

					$css .= $option['media_query'] .'{'. $option['element'] .'{ '. $option['style'] .':'. $theme_mod.' !important; } }';
				} else {
					$css .= $option['element'] .'{ '. $option['style'] .':'. $theme_mod.' !important; }';
				}
			}
		}
		$css =  preg_replace( '/\s+/', ' ', $css );
		$css = "<!-- Theme Customizer Styling Options -->\n<style type=\"text/css\">\n" . $css . "\n</style>";
		if ( !empty( $css ) ) {
			echo $css;
		}
	} // End header_output function


	/**
	* Array of styling options
	* 
	* @since Fabulous 1.0
	*/
	public static function wpex_color_options() {

		$array = array();

		$array[] = array(
			'label'		=> __( 'Header Top Padding', 'wpex' ),
			'id'		=> 'header_top_pad',
			'element'	=> '#header-wrap',
			'style'		=> 'padding-top',
			'type'		=> 'text',
			'default'	=> '',
		);

		$array[] = array(
			'label'		=> __( 'Header Bottom Padding', 'wpex' ),
			'id'		=> 'header_bottom_pad',
			'element'	=> '#header-wrap',
			'style'		=> 'padding-bottom',
			'type'		=> 'text',
			'default'	=> '',
		);

		$array[] = array(
			'label'		=> __( 'Logo Text Color', 'wpex' ),
			'id'		=> 'logo_color',
			'element'	=> '#logo a',
			'style'		=> 'color',
		);

		$array[] = array(
			'label'		=> __( 'Menu Link Color', 'wpex' ),
			'id'		=> 'nav_link_color',
			'element'	=> '#site-navigation .dropdown-menu > li > a',
			'style'		=> 'color',
		);

		$array[] = array(
			'label'		=> __( 'Menu Link Hover Color', 'wpex' ),
			'id'		=> 'nav_link_hover_color',
			'element'	=> '#site-navigation .dropdown-menu > li > a:hover',
			'style'		=> 'color',
		);

		$array[] = array(
			'label'		=> __( 'Active Menu Link Color', 'wpex' ),
			'id'		=> 'nav_link_active_color',
			'element'	=> '#site-navigation .dropdown-menu > li > a:hover,#site-navigation .dropdown-menu > li.sfHover > a,#site-navigation .dropdown-menu > .current-menu-item > a,#site-navigation .dropdown-menu > .current-menu-item > a:hover ',
			'style'		=> 'color',
		);

		$array[] = array(
			'label'		=> __( 'Sub-Menu Background', 'wpex' ),
			'id'		=> 'nav_drop_bg',
			'element'	=> '#site-navigation .dropdown-menu ul',
			'style'		=> 'background',
		);

		$array[] = array(
			'label'		=> __( 'Sub-Menu Link Bottom Border', 'wpex' ),
			'id'		=> 'nav_drop_link_border',
			'element'	=> '#site-navigation .dropdown-menu ul li',
			'style'		=> 'border-color',
		);

		$array[] = array(
			'label'		=> __( 'Sub-Menu Link Color', 'wpex' ),
			'id'		=> 'nav_drop_link_color',
			'element'	=> '#site-navigation .dropdown-menu ul > li > a',
			'style'		=> 'color',
		);

		$array[] = array(
			'label'		=> __( 'Sub-Menu Link Hover Color', 'wpex' ),
			'id'		=> 'nav_drop_link_hover_color',
			'element'	=> '#site-navigation .dropdown-menu ul > li > a:hover',
			'style'		=> 'color',
		);

		$array[] = array(
			'label'		=> __( 'Sub-Menu Link Hover Background', 'wpex' ),
			'id'		=> 'nav_drop_link_hover_bg',
			'element'	=> '#site-navigation .dropdown-menu ul > li > a:hover',
			'style'		=> 'background',
		);

		$array[] = array(
			'label'		=> __( 'Mobile Menu Link Color', 'wpex' ),
			'id'		=> 'mobile_nav_link_color',
			'element'	=> 'a#navigation-toggle',
			'style'		=> 'color',
		);

		$array[] = array(
			'label'		=> __( 'Footer Widgets Background', 'wpex' ),
			'id'		=> 'footer_widgets_bg',
			'element'	=> '#footer-wrap',
			'style'		=> 'background',
		);

		$array[] = array(
			'label'		=> __( 'Footer Widgets Text', 'wpex' ),
			'id'		=> 'footer_widgets_color',
			'element'	=> 'footer, #footer p',
			'style'		=> 'color',
		);

		$array[] = array(
			'label'		=> __( 'Footer Widgets Heading', 'wpex' ),
			'id'		=> 'footer_widgets_headings',
			'element'	=> '#footer h2, #footer h3, #footer h4, #footer h5,  #footer h6, #footer-widgets .widget-title',
			'style'		=> 'color',
		);

		$array[] = array(
			'label'		=> __( 'Footer Widgets Links', 'wpex' ),
			'id'		=> 'footer_widgets_links_color',
			'element'	=> '#footer a, #footer-widgets .widget_nav_menu ul > li li a:before',
			'style'		=> 'color',
		);

		$array[] = array(
			'label'		=> __( 'Footer Widgets Links Hover', 'wpex' ),
			'id'		=> 'footer_widgets_links_hover_color',
			'element'	=> '#footer a:hover',
			'style'		=> 'color',
		);

		$array[] = array(
			'label'		=> __( 'Footer Widgets Borders', 'wpex' ),
			'id'		=> 'footer_widgets_borders',
			'element'	=> '#footer-widgets .widget_nav_menu ul > li, #footer-widgets .widget_nav_menu ul > li a, .footer-widget > ul > li:first-child, .footer-widget > ul > li, .footer-widget h6, #footer-bottom',
			'style'		=> 'border-color',
		);

		$array[] = array(
			'label'		=> __( 'Copyright Backgorund', 'wpex' ),
			'id'		=> 'copyright_bg',
			'element'	=> '#copyright-wrap',
			'style'		=> 'background-color',
		);

		$array[] = array(
			'label'		=> __( 'Copyright Color', 'wpex' ),
			'id'		=> 'copyright_color',
			'element'	=> '#copyright-wrap, #copyright-wrap p',
			'style'		=> 'color',
		);

		$array[] = array(
			'label'		=> __( 'Copyright Link Color', 'wpex' ),
			'id'		=> 'copyright_link_color',
			'element'	=> '#copyright-wrap a',
			'style'		=> 'color',
		);

		$array[] = array(
			'label'		=> __( 'Heading Title Hover Color', 'wpex' ),
			'id'		=> 'heading_title_hover_color',
			'element'	=> 'h1 a:hover, h2 a:hover, h3 a:hover, h4 a:hover',
			'style'		=> 'color',
		);

		$array[] = array(
			'label'		=> __( 'Link Color', 'wpex' ),
			'id'		=> 'link_color',
			'element'	=> '.single .entry a, #sidebar a, .comment-meta a.url, .logged-in-as a',
			'style'		=> 'color',
		);

		$array[] = array(
			'label'		=> __( 'Link Hover Color', 'wpex' ),
			'id'		=> 'link_hover_color',
			'element'	=> '.single .entry a:hover, #sidebar a:hover, .comment-meta a.url:hover, .logged-in-as a:hover',
			'style'		=> 'color',
		);

		$array[] = array(
			'label'		=> __( 'Sidebar Link Color', 'wpex' ),
			'id'		=> 'sidebar_link_color',
			'element'	=> '.sidebar-container a',
			'style'		=> 'color',
		);

		$array[] = array(
			'label'		=> __( 'Sidebar Link Hover Color', 'wpex' ),
			'id'		=> 'sidebar_link_hover_color',
			'element'	=> '.sidebar-container a:hover',
			'style'		=> 'color',
		);

		$array[] = array(
			'label'		=> __( 'Theme Button Color', 'wpex' ),
			'id'		=> 'theme_button_color',
			'element'	=> '.wpex-readmore a, input[type="button"], input[type="submit"], .page-numbers a:hover, .page-numbers.current, .page-links span, .page-links a:hover span',
			'style'		=> 'color',
		);

		$array[] = array(
			'label'		=> __( 'Theme Button Background', 'wpex' ),
			'id'		=> 'theme_button_bg',
			'element'	=> '.wpex-readmore a, input[type="button"], input[type="submit"], .page-numbers a:hover, .page-numbers.current, .page-links span, .page-links a:hover span',
			'style'		=> 'background',
		);

		$array[] = array(
			'label'		=> __( 'Theme Button Hover Color', 'wpex' ),
			'id'		=> 'theme_button_hover_color',
			'element'	=> '.wpex-readmore a:hover, input[type="button"]:hover, input[type="submit"]:hover',
			'style'		=> 'color',
		);

		$array[] = array(
			'label'		=> __( 'Theme Button Hover Background', 'wpex' ),
			'id'		=> 'theme_button_hover_bg',
			'element'	=> '.wpex-readmore a:hover, input[type="button"]:hover, input[type="submit"]:hover',
			'style'		=> 'background-color',
		);

		$array[] = array(
			'label'		=> __( 'Homepage Icons', 'wpex' ),
			'id'		=> 'home_icons_color',
			'element'	=> '.features-entry .feature-icon-font .fa',
			'style'		=> 'color',
		);

		$array[] = array(
			'label'		=> __( 'Homepage Slider Arrows Hover Background', 'wpex' ),
			'id'		=> 'home_slider_arrow_hover_bg',
			'element'	=> '#homepage-slider-wrap .flex-direction-nav li a:hover',
			'style'		=> 'background',
		);

		// Apply filters for child theming magic
		$array = apply_filters( 'wpex_color_options_array', $array );

		// Return array
		return $array;
	}

} // End Theme_Customizer_Styling Class


// Setup the Theme Customizer settings and controls
add_action( 'customize_register' , array( 'WPEX_Theme_Customizer_Styling' , 'register' ) );

// Output custom CSS to live site
add_action( 'wp_head' , array( 'WPEX_Theme_Customizer_Styling' , 'header_output' ) );



/**
* Remove Inner shadow for buttons if their colors
* have been altered via the customizer
* 
* @since Fabulous 1.0
*/
if ( ! function_exists('wpex_remove_button_shadow') ) {
	function wpex_remove_button_shadow() {
		$css='';
		if ( '' != get_theme_mod( 'wpex_theme_button_bg' ) ) {
			$css = 'input[type="button"], input[type="submit"], .page-numbers a:hover, .page-numbers.current, .page-links span, .page-links a:hover span { box-shadow: 0 1px 2px rgba(0,0,0,0.07); }';
		}
		if ( $css ) {
			$css =  preg_replace( '/\s+/', ' ', $css );
			$css = "<!-- Remove Button Box Shadow -->\n<style type=\"text/css\">\n" . $css . "\n</style>";
			echo $css;
		} else {
			return;
		}

	}
}


// Output custom CSS to live site
add_action( 'wp_head' , 'wpex_remove_button_shadow' );